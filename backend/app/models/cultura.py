from app import db


class Cultura(db.Model):
    __tablename__ = "culturas"

    id = db.Column(db.Integer, primary_key=True)

    nome_cultura = db.Column(db.String(100), nullable=False)
    area_plantada = db.Column(db.Float, nullable=False)

    propriedade_id = db.Column(
        db.Integer,
        db.ForeignKey("propriedades.id"),
        nullable=False
    )