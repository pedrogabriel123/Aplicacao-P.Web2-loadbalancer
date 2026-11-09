from app.models.propriedade import Propriedade

class PropriedadeRepository:

    @staticmethod
    def save(propriedade):
        from app import db
        db.session.add(propriedade)
        db.session.commit()
        return propriedade

    @staticmethod
    def find_by_id(id):
        return Propriedade.query.get(id)

    @staticmethod
    def delete(propriedade):
        from app import db
        db.session.delete(propriedade)
        db.session.commit()

    @staticmethod
    def find_filtered(nome=None, produtor_id=None, page=1, per_page=5):
        query = Propriedade.query

        if nome:
            query = query.filter(Propriedade.nome.ilike(f"%{nome}%"))

        if produtor_id:
            query = query.filter(Propriedade.produtor_id == produtor_id)

        return query.paginate(page=page, per_page=per_page, error_out=False)