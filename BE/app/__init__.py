import os
from flask import Flask, Blueprint, url_for, jsonify, redirect
import BE.settings as settings
from BE.app.api.endpoints.images import ns as image_ns
from flask_restx import Api
from BE.app.api.auth.auth import auth_ns
from BE.app.extensions import bcrypt, cors, db, jwt, ma


authorizations = {
    'Bearer Auth': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    },
}
api = Api(version='0.1', title='Backend API', security='Bearer Auth', authorizations=authorizations, description='Backend API for sticker generation')





#app.wsgi_app = ProxyFix(app.wsgi_app)

#flask_restx API supports prior flask_restplus api
def configure_app(app):
    if not os.path.exists(settings.UPLOAD_FOLDER):
        try:
            os.mkdir(settings.UPLOAD_FOLDER)
        except OSError:
            print("Creation of the directory %s failed" % settings.UPLOAD_FOLDER)
    app.secret_key = '123'
    app.config['SWAGGER_UI_DOC_EXPANSION'] = settings.RESTPLUS_SWAGGER_EXPANSION
    app.config['RESTX_VALIDATE'] = settings.RESTPLUS_VAL
    app.config['RESTX_MASK_SWAGGER'] = settings.RESTPLUS_MASK_SWAGGER
    app.config['SQLALCHEMY_DATABASE_URI'] = settings.SQLALCHEMY_DATABASE_URI
    app.config['UPLOAD_FOLDER'] = settings.UPLOAD_FOLDER
    app.config['MAX_UPLOAD_LENGTH'] = 24 * 1024 * 1024  # limits filesize to 24 mb
    app.config['SESSION_TYPE'] = settings.SESSION_TYPE
    app.config['SQLALCHEMY_TRACK_MODS'] = settings.SQLALCHEMY_TRACK_MODS

def register_extensions(app):
    # Registers flask extensions
    db.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)
    cors.init_app(app)

def init_app(app):
    #db.reset()
    configure_app(app)
    api_blueprint = Blueprint('api', __name__, url_prefix='/api')
    api.add_namespace(image_ns)
    api.add_namespace(auth_ns)
    api.init_app(api_blueprint)
    app.register_blueprint(api_blueprint)
    register_extensions(app)

def has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)



def create_app():
    app = Flask(__name__)
    @app.before_first_request
    def create_tables():
        db.create_all()
    configure_app(app)
    init_app(app)

    @app.route('/')
    def home():
        return redirect('/api')

    return app

if __name__ == '__main__':
    app = create_app()
    context = ('server.crt', 'server.key')
    print(context)
    app.run(debug=True, ssl_context=context)
