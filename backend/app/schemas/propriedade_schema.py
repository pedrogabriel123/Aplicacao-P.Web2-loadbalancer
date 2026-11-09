# app/schemas/propriedade_schema.py
from app import ma
from app.models.propriedade import Propriedade

class PropriedadeSchema(ma.SQLAlchemyAutoSchema):
    culturas = ma.Nested('CulturaSchema', many=True, exclude=('propriedade',))

    class Meta:
        model = Propriedade
        load_instance = True
        include_fk = True

propriedade_schema = PropriedadeSchema()
propriedades_schema = PropriedadeSchema(many=True)