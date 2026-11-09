import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from .config import Config

db = SQLAlchemy()
ma = Marshmallow()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    ma.init_app(app)

    # IMPORTANTE: importa os models para registrar no metadata
    from app import models

   
    with app.app_context():
        db.create_all()

    logging.basicConfig(
        level=app.config["LOG_LEVEL"],
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    )

    app.logger.info("Aplicação iniciada com sucesso.")

    from .resources.produtor_resource import produtor_bp
    from .resources.propriedade_resource import propriedade_bp
    from .resources.cultura_resource import cultura_bp

    app.register_blueprint(produtor_bp)
    app.register_blueprint(propriedade_bp)
    app.register_blueprint(cultura_bp)

    return app