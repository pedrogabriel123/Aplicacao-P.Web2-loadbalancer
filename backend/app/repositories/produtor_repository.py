from app.models.produtor import Produtor

class ProdutorRepository:

    @staticmethod
    def save(produtor):
        from app import db
        db.session.add(produtor)
        db.session.commit()
        return produtor

    @staticmethod
    def find_by_id(id):
        return Produtor.query.get(id)

    @staticmethod
    def delete(produtor):
        from app import db
        db.session.delete(produtor)
        db.session.commit()

    @staticmethod
    def find_filtered(nome=None, idade=None, page=1, per_page=5):
        query = Produtor.query

        if nome:
            query = query.filter(Produtor.nome.ilike(f"%{nome}%"))

        if idade:
            query = query.filter(Produtor.idade == idade)

        return query.paginate(page=page, per_page=per_page, error_out=False)