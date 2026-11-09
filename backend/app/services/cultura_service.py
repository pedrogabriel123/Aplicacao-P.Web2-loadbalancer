from app import db
from app.models.cultura import Cultura


class CulturaService:

    @staticmethod
    def listar(nome_cultura, propriedade_id, page, per_page):
        query = Cultura.query

        if nome_cultura:
            query = query.filter(Cultura.nome_cultura.ilike(f"%{nome_cultura}%"))

        if propriedade_id:
            query = query.filter_by(propriedade_id=propriedade_id)

        return query.paginate(page=page, per_page=per_page)


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