from app import create_app, db
from app.models.produtor import Produtor
from app.models.propriedade import Propriedade
from app.models.cultura import Cultura
from datetime import date
from sqlalchemy import text

app = create_app()

with app.app_context():

    db.session.execute(text("TRUNCATE TABLE culturas RESTART IDENTITY CASCADE;"))
    db.session.execute(text("TRUNCATE TABLE propriedades RESTART IDENTITY CASCADE;"))
    db.session.execute(text("TRUNCATE TABLE produtores RESTART IDENTITY CASCADE;"))
    db.session.commit()
    
    # =========================
    # PRODUTORES (com data_nascimento)
    # =========================
    produtores = [
        Produtor(nome="João Silva", cpf="11111111111", data_nascimento=date(1979, 5, 10)),
        Produtor(nome="Maria Oliveira", cpf="22222222222", data_nascimento=date(1986, 3, 22)),
        Produtor(nome="Carlos Santos", cpf="33333333333", data_nascimento=date(1974, 8, 15)),
        Produtor(nome="Ana Souza", cpf="44444444444", data_nascimento=date(1982, 11, 3)),
        Produtor(nome="Pedro Lima", cpf="55555555555", data_nascimento=date(1989, 1, 27)),
        Produtor(nome="Juliana Costa", cpf="66666666666", data_nascimento=date(1995, 6, 18)),
        Produtor(nome="Rafael Alves", cpf="77777777777", data_nascimento=date(1969, 9, 9)),
        Produtor(nome="Camila Rocha", cpf="88888888888", data_nascimento=date(1992, 4, 12)),
        Produtor(nome="Lucas Pereira", cpf="99999999999", data_nascimento=date(1984, 7, 30)),
        Produtor(nome="Fernanda Martins", cpf="00000000000", data_nascimento=date(1988, 2, 5)),
    ]

    db.session.add_all(produtores)
    db.session.commit()

    # =========================
    # PROPRIEDADES (estado + município detalhado)
    # =========================
    propriedades = [
        Propriedade(
        nome="Fazenda Boa Vista",
        tamanho_hectares=120.5,
        municipio_nome="Campina Grande",
        municipio_codigo="2504009",
        estado_nome="Paraíba",
        estado_uf="PB",
        produtor_id=1
    ),
    Propriedade(
        nome="Sítio Verde",
        tamanho_hectares=80.0,
        municipio_nome="Patos",
        municipio_codigo="2510808",
        estado_nome="Paraíba",
        estado_uf="PB",
        produtor_id=2
    ),
    Propriedade(
        nome="Chácara Feliz",
        tamanho_hectares=50.2,
        municipio_nome="Sousa",
        municipio_codigo="2516201",
        estado_nome="Paraíba",
        estado_uf="PB",
        produtor_id=3
    ),
    Propriedade(
        nome="Fazenda Horizonte",
        tamanho_hectares=200.0,
        municipio_nome="Pombal",
        municipio_codigo="2512101",
        estado_nome="Paraíba",
        estado_uf="PB",
        produtor_id=4
    ),
    Propriedade(
        nome="Sítio do Sol",
        tamanho_hectares=75.0,
        municipio_nome="Itaporanga",
        municipio_codigo="2507002",
        estado_nome="Paraíba",
        estado_uf="PB",
        produtor_id=5
    ),
    Propriedade(
        nome="Fazenda Nova Era",
        tamanho_hectares=150.0,
        municipio_nome="Queimadas",
        municipio_codigo="2513000",
        estado_nome="Paraíba",
        estado_uf="PB",
        produtor_id=6
    ),
    Propriedade(
        nome="Chácara Primavera",
        tamanho_hectares=60.0,
        municipio_nome="Campina Grande",
        municipio_codigo="2504009",
        estado_nome="Paraíba",
        estado_uf="PB",
        produtor_id=7
    ),
    Propriedade(
        nome="Sítio das Flores",
        tamanho_hectares=90.0,
        municipio_nome="Patos",
        municipio_codigo="2510808",
        estado_nome="Paraíba",
        estado_uf="PB",
        produtor_id=8
    ),
    Propriedade(
        nome="Fazenda Paraíso",
        tamanho_hectares=180.0,
        municipio_nome="Sousa",
        municipio_codigo="2516201",
        estado_nome="Paraíba",
        estado_uf="PB",
        produtor_id=9
    ),
    Propriedade(
        nome="Chácara Alegre",
        tamanho_hectares=55.0,
        municipio_nome="Pombal",
        municipio_codigo="2512101",
        estado_nome="Paraíba",
        estado_uf="PB",
        produtor_id=10
    ),
    ]

    db.session.add_all(propriedades)
    db.session.commit()

    # =========================
    # CULTURAS
    # =========================
    culturas = [
        Cultura(nome_cultura="Milho", area_plantada=20.0, propriedade_id=1),
        Cultura(nome_cultura="Soja", area_plantada=35.0, propriedade_id=2),
        Cultura(nome_cultura="Feijão", area_plantada=15.0, propriedade_id=3),
        Cultura(nome_cultura="Trigo", area_plantada=50.0, propriedade_id=4),
        Cultura(nome_cultura="Cana-de-açúcar", area_plantada=40.0, propriedade_id=5),
        Cultura(nome_cultura="Algodão", area_plantada=30.0, propriedade_id=6),
        Cultura(nome_cultura="Tomate", area_plantada=10.0, propriedade_id=7),
        Cultura(nome_cultura="Batata", area_plantada=25.0, propriedade_id=8),
        Cultura(nome_cultura="Cenoura", area_plantada=12.0, propriedade_id=9),
        Cultura(nome_cultura="Laranja", area_plantada=18.0, propriedade_id=10),
    ]

    db.session.add_all(culturas)
    db.session.commit()

    print("Banco populado com sucesso! ✅")