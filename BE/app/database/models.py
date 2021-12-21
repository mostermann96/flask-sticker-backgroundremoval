from BE.app.extensions import db, ma

"""
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000), unique=True)
"""

class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(1000))
    filepath = db.Column(db.String(1000))
    db.UniqueConstraint('username', 'filepath')





class UserSchema(ma.Schema):
    class Meta:
        # Fields to expose, add more if needed. deleted role_id
        fields = ("email", "name", "username", "joined_date")
def init_db():
    db.create_all()

if __name__ == '__main__':
    init_db()