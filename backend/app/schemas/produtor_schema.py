from app import ma
from app.models.produtor import Produtor

class ProdutorSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Produtor
        load_instance = True

produtor_schema = ProdutorSchema()
produtores_schema = ProdutorSchema(many=True)