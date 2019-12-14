import os
from app import db
from app.models import User

ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD') or "supersecret"
u = User(username='admin')
u.set_password(ADMIN_PASSWORD)
u.set_password2("12345678901")
db.session.add(u)
db.session.commit()
