from flask import current_app
from app.repositories.propriedade_repository import PropriedadeRepository

class PropriedadeService:

    @staticmethod
    def listar(nome, produtor_id, page, per_page):
        current_app.logger.info(f"Listando propriedades | filtros aplicados")
        return PropriedadeRepository.find_filtered(nome, produtor_id, page, per_page)

    @staticmethod
    def buscar_por_id(id):
        current_app.logger.info(f"Buscando propriedade ID {id}")
        return PropriedadeRepository.find_by_id(id)

    @staticmethod
    def salvar(propriedade):
        current_app.logger.info("Salvando propriedade")
        return PropriedadeRepository.save(propriedade)

    @staticmethod
    def deletar(propriedade):
        current_app.logger.warning(f"Removendo propriedade {propriedade.id}")
        PropriedadeRepository.delete(propriedade)