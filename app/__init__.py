from flask import Flask

def create_app():
    app = Flask(__name__)

    from .routes import pdf_blueprint
    app.register_blueprint(pdf_blueprint)

    return app
