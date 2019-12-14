from datetime import datetime
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    password2_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    logins = db.relationship('Login', backref='author')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def set_password2(self, password2):
        self.password2_hash = generate_password_hash(password2)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def check_password2(self, password2):
        return check_password_hash(self.password2_hash, password2)

    def spellcheck_posts(self):
        return Post.query.filter_by(user_id=self.id).order_by(Post.timestamp.desc())

    def spellcheck_posts_all(self):
        return Post.query.order_by(Post.timestamp.desc())

    def login_logs(self, id):
        print("id",id)
        return Login.query.filter_by(user_id=id)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(1000))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    result = db.Column(db.String(1000))

    def __repr__(self):
        return '<Post {}>'.format(self.body)

class Login(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login_timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    logout_timestamp = db.Column(db.DateTime, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

@login.user_loader
def load_user(id):
    return User.query.get(int(id))
