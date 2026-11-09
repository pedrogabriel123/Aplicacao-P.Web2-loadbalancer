from flask import Blueprint, request
from app.schemas.propriedade_schema import propriedade_schema, propriedades_schema
from app.services.propriedade_service import PropriedadeService

propriedade_bp = Blueprint("propriedade_bp", __name__, url_prefix="/propriedades")


@propriedade_bp.route("", methods=["GET"])
def listar_propriedades():
    nome = request.args.get("nome")
    produtor_id = request.args.get("produtor_id", type=int)
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 5, type=int)

    pagination = PropriedadeService.listar(nome, produtor_id, page, per_page)

    return {
        "data": propriedades_schema.dump(pagination.items),
        "pagination": {
            "total": pagination.total,
            "page": pagination.page,
            "pages": pagination.pages,
            "per_page": per_page
        }
    }


@propriedade_bp.route("/<int:id>", methods=["GET"])
def buscar_propriedade(id):
    propriedade = PropriedadeService.buscar_por_id(id)

    if not propriedade:
        return {"message": "Propriedade não encontrada"}, 404

    return {
        "data": propriedade_schema.dump(propriedade),
        "links": {
            "self": f"/propriedades/{id}",
            "propriedades": f"/produtores/{propriedade.produtor_id}/propriedades"
        }
    }


@propriedade_bp.route("", methods=["POST"])
def criar_propriedade():
    propriedade = propriedade_schema.load(request.json)
    propriedade = PropriedadeService.salvar(propriedade)

    return {
        "data": propriedade_schema.dump(propriedade),
        "message": "Propriedade criada com sucesso"
    }, 201


@propriedade_bp.route("/<int:id>", methods=["PUT"])
def atualizar_propriedade(id):
    propriedade = PropriedadeService.buscar_por_id(id)

    if not propriedade:
        return {"message": "Propriedade não encontrada"}, 404

    data = request.json
    propriedade.nome = data["nome"]
    propriedade.tamanho_hectares = data["tamanho_hectares"]
    propriedade.cidade = data["cidade"]
    propriedade.estado = data["estado"]
    propriedade.produtor_id = data["produtor_id"]

    PropriedadeService.salvar(propriedade)

    return {"data": propriedade_schema.dump(propriedade)}


@propriedade_bp.route("/<int:id>", methods=["PATCH"])
def atualizar_parcial(id):
    propriedade = PropriedadeService.buscar_por_id(id)

    if not propriedade:
        return {"message": "Propriedade não encontrada"}, 404

    data = request.json

    if "nome" in data:
        propriedade.nome = data["nome"]
    if "tamanho_hectares" in data:
        propriedade.tamanho_hectares = data["tamanho_hectares"]
    if "cidade" in data:
        propriedade.cidade = data["cidade"]
    if "estado" in data:
        propriedade.estado = data["estado"]
    if "produtor_id" in data:
        propriedade.produtor_id = data["produtor_id"]

    PropriedadeService.salvar(propriedade)

    return {"data": propriedade_schema.dump(propriedade)}


@propriedade_bp.route("/<int:id>", methods=["DELETE"])
def deletar_propriedade(id):
    propriedade = PropriedadeService.buscar_por_id(id)

    if not propriedade:
        return {"message": "Propriedade não encontrada"}, 404

    PropriedadeService.deletar(propriedade)

    return {}, 204