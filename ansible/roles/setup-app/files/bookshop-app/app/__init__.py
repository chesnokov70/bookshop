from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    db.init_app(app)

    with app.app_context():
        from app.routes import bp  # <-- ИСПРАВЛЕНО
        app.register_blueprint(bp)

        # Можно создать таблицы, если они не существуют
        db.create_all()

    return app
