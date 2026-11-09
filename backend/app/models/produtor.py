from datetime import date
from app import db


class Produtor(db.Model):
    __tablename__ = "produtores"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)

    # CPF com 11 dígitos e único
    cpf = db.Column(db.String(11), nullable=False, unique=True)

    # Agora idade vem da data
    data_nascimento = db.Column(db.Date, nullable=False)

    propriedades = db.relationship(
        "Propriedade",
        backref="produtor",
        lazy=True,
        cascade="all, delete-orphan"
    )

    @property
    def idade(self):
        hoje = date.today()
        return (
            hoje.year
            - self.data_nascimento.year
            - (
                (hoje.month, hoje.day)
                < (self.data_nascimento.month, self.data_nascimento.day)
            )
        )