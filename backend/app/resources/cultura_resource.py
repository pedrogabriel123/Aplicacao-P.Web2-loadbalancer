from flask import Blueprint, request
from app.schemas.cultura_schema import cultura_schema, culturas_schema
from app.services.cultura_service import CulturaService

cultura_bp = Blueprint("cultura_bp", __name__, url_prefix="/culturas")



@cultura_bp.route("", methods=["GET"])
def listar_culturas():
    nome_cultura = request.args.get("nome_cultura")
    propriedade_id = request.args.get("propriedade_id", type=int)
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 5, type=int)

    pagination = CulturaService.listar(nome_cultura, propriedade_id, page, per_page)

    return {
        "data": culturas_schema.dump(pagination.items),
        "pagination": {
            "total": pagination.total,
            "page": pagination.page,
            "pages": pagination.pages,
            "per_page": per_page
        }
    }



@cultura_bp.route("/<int:id>", methods=["GET"])
def buscar_cultura(id):
    cultura = CulturaService.buscar_por_id(id)

    if not cultura:
        return {"message": "Cultura não encontrada"}, 404

    return {
        "data": cultura_schema.dump(cultura),
        "links": {
            "self": f"/culturas/{id}",
            "propriedade": f"/propriedades/{cultura.propriedade_id}"
        }
    }



@cultura_bp.route("", methods=["POST"])
def criar_cultura():
    cultura = cultura_schema.load(request.json)
    cultura = CulturaService.salvar(cultura)

    return {
        "data": cultura_schema.dump(cultura),
        "message": "Cultura criada com sucesso"
    }, 201



@cultura_bp.route("/<int:id>", methods=["PUT"])
def atualizar_cultura(id):
    cultura = CulturaService.buscar_por_id(id)

    if not cultura:
        return {"message": "Cultura não encontrada"}, 404

    data = request.json
    cultura.nome_cultura = data["nome_cultura"]
    cultura.area_plantada = data["area_plantada"]
    cultura.propriedade_id = data["propriedade_id"]

    CulturaService.salvar(cultura)

    return {"data": cultura_schema.dump(cultura)}



@cultura_bp.route("/<int:id>", methods=["PATCH"])
def atualizar_parcial(id):
    cultura = CulturaService.buscar_por_id(id)

    if not cultura:
        return {"message": "Cultura não encontrada"}, 404

    data = request.json

    if "nome_cultura" in data:
        cultura.nome_cultura = data["nome_cultura"]
    if "area_plantada" in data:
        cultura.area_plantada = data["area_plantada"]
    if "propriedade_id" in data:
        cultura.propriedade_id = data["propriedade_id"]

    CulturaService.salvar(cultura)

    return {"data": cultura_schema.dump(cultura)}



@cultura_bp.route("/<int:id>", methods=["DELETE"])
def deletar_cultura(id):
    cultura = CulturaService.buscar_por_id(id)

    if not cultura:
        return {"message": "Cultura não encontrada"}, 404

    CulturaService.deletar(cultura)

    return {}, 204