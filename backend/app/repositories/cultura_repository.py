from app.models.cultura import Cultura
from app import db

class CulturaRepository:
    @staticmethod
    def listar_filtros(nome_cultura=None, propriedade_id=None):
        query = Cultura.query
        if nome_cultura:
            query = query.filter(Cultura.nome_cultura.ilike(f"%{nome_cultura}%"))
        if propriedade_id:
            query = query.filter(Cultura.propriedade_id == propriedade_id)
        return query

    @staticmethod
    def buscar_por_id(id):
        return Cultura.query.get(id)

    @staticmethod
    def salvar(cultura):
        db.session.add(cultura)
        db.session.commit()
        return cultura

    @staticmethod
    def deletar(cultura):
        db.session.delete(cultura)
        db.session.commit()