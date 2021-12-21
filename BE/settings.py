from os.path import join, dirname, realpath

FLASK_SERVER_NAME = 'https://localhost:5000'
FLASK_DEBUG = True #CHANGE BEFORE DEPLOYMENT
FLASK_THREADED = False

RESTPLUS_SWAGGER_EXPANSION = 'list'
RESTPLUS_VAL = True
RESTPLUS_MASK_SWAGGER = False
UPLOAD_FOLDER = join(dirname(realpath(__file__)), 'images')
SESSION_TYPE = 'filesystem'

SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite'
SQLALCHEMY_TRACK_MODS = False
