from flask_sqlalchemy import SQLAlchemy
from BE.app.extensions import db
#from .models import Image


def reset():
    db.drop_all()
    db.create_all()
#def check():

def add(db_image):
    db.session.add(db_image)
    db.session.commit()

"""def add_image(name, filepath):
    db.session.add(Image(name,filepath))
    db.session.commit()"""

def delete(db_image):
    db.session.remove(db_image)
    db.session.commit()

#update is written manually