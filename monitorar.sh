
#!/bin/bash

# Censo Agricola - Monitoramento em tempo real
# Acompanha os cinco frontends e o backend Flask.

python3 -u - <<'PY'
import subprocess
import threading
import queue
import re
import time
import os
import shutil
from collections import Counter, deque
from datetime import datetime

CONTAINERS = ["no1", "no2", "no3", "no4", "no5"]
BACKEND = "censo-agricula-api"
TODOS = CONTAINERS + [BACKEND]

eventos = queue.Queue()
contadores = Counter()
erros = 0
historico = deque(maxlen=12)
processos = []
encerrar = threading.Event()

PADRAO = re.compile(
    r'"([A-Z]+)\s*(.*?)\s+HTTP/[^"]+"\s+(\d{3})'
)

def acompanhar(container):
    try:
        processo = subprocess.Popen(
            ["docker", "logs", "-f", "--tail", "0",
             "--timestamps", container],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )

        processos.append(processo)

        for linha in processo.stdout:
            if encerrar.is_set():
                break

            resultado = PADRAO.search(linha)

            if not resultado:
                continue

            metodo, rota, status = resultado.groups()

            eventos.put({
                "container": container,
                "metodo": metodo,
                "rota": rota,
                "status": int(status),
                "hora": datetime.now().strftime("%H:%M:%S")
            })

    except Exception as erro:
        eventos.put({"falha": f"{container}: {erro}"})

def desenhar():
    largura = min(shutil.get_terminal_size((100, 30)).columns, 110)

    os.system("clear")
    print("=" * largura)
    print("             CENSO AGRICOLA | LIVE MONITOR")
    print("                 DOCKER LOAD BALANCER")
    print("=" * largura)

    total_frontend = sum(contadores[n] for n in CONTAINERS)
    total_api = contadores[BACKEND]
    total = total_frontend + total_api

    print(f"\n  STATUS: MONITORAMENTO ATIVO")
    print(f"  FRONTENDS: 5       BACKEND: 1       TOTAL: 6")
    print(f"  REQUISICOES: {total}       ERROS HTTP: {erros}")
    print("\n" + "-" * largura)
    print("  DISTRIBUICAO DOS FRONTENDS")
    print("-" * largura)

    for nome in CONTAINERS:
        quantidade = contadores[nome]
        percentual = (
            quantidade / total_frontend * 100
            if total_frontend else 0
        )
        barras = int(percentual / 5)
        grafico = "#" * barras + "-" * (20 - barras)

        print(
            f"  {nome:5} [{grafico}] "
            f"{quantidade:5} requisicoes ({percentual:5.1f}%)"
        )

    print("\n" + "-" * largura)
    print("  BACKEND FLASK")
    print("-" * largura)
    print(f"  {BACKEND}: {total_api} requisicoes")

    print("\n" + "-" * largura)
    print("  HISTORICO DE REQUISICOES")
    print("-" * largura)

    if not historico:
        print("  Aguardando requisicoes...")

    for evento in historico:
        print(evento)

    print("\n" + "=" * largura)
    print("  Atualizacao automatica | CTRL+C para encerrar")
    print("=" * largura)

def main():
    global erros

    print("Iniciando monitoramento dos containers...")

    for container in TODOS:
        thread = threading.Thread(
            target=acompanhar,
            args=(container,),
            daemon=True
        )
        thread.start()

    time.sleep(1)

    try:
        while True:
            recebeu_evento = False

            while True:
                try:
                    evento = eventos.get_nowait()
                except queue.Empty:
                    break

                if "falha" in evento:
                    historico.append(
                        f"[AVISO] {evento['falha']}"
                    )
                    continue

                nome = evento["container"]
                status = evento["status"]

                contadores[nome] += 1

                if status >= 400:
                    erros += 1

                tipo = "BACKEND" if nome == BACKEND else "FRONTEND"

                historico.append(
                    f"[{evento['hora']}] {tipo:8} "
                    f"{nome:18} {evento['metodo']:6} "
                    f"{evento['rota']} | HTTP {status}"
                )

                recebeu_evento = True

            desenhar()
            time.sleep(1)

    except KeyboardInterrupt:
        pass

    finally:
        encerrar.set()

        for processo in processos:
            processo.terminate()

        print("\nMonitoramento encerrado.")
        print(f"Total de requisicoes: {sum(contadores.values())}")
        print(f"Erros HTTP: {erros}")

if __name__ == "__main__":
    main()
PY
