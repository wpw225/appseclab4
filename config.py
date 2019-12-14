import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Enable protection against CSRF
    CSRF_ENABLED = True

    # Use a secure, unique secret key for signing data
    CSRF_SESSION_KEY = os.environ.get('CSRF_SESSION_KEY') or "csrf_secret"
#    print("CSRF_KEY:", CSRF_SESSION_KEY)

    # Secret key for signing cookies
    SECRET_KEY = os.environ.get('SECRET_KEY') or "key_secret"
#    print("KEY:", SECRET_KEY)
