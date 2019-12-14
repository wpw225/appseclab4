from flask import render_template, flash, redirect, url_for, request
from app import app
from app.forms import LoginForm
from flask_login import current_user, login_user
from flask_login import logout_user
from flask_login import login_required
from app.models import User
from app import db
from app.forms import RegistrationForm
from app.forms import PostForm
from app.forms import HistoryForm
from app.forms import LoginHistoryForm
from app.models import Post
from app.models import Login
#from urlparse import urlparse
from urllib.parse import urlparse
from subprocess import check_output
#from talisman import Talisman,ALLOW_FROM
from datetime import datetime

SELF = "'self'"
print(SELF)
#talisman = Talisman(
#    app,
#    content_security_policy={
#        'default-src': SELF,
#        'img-src': '*',
#        'script-src': SELF,
#        'style-src': [
#            SELF
#        ],
#    },
#    force_https=True,
#    force_https_permanent=False,
#    strict_transport_security=False
#)

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@app.route('/spell_check', methods=['GET', 'POST'])
@login_required
#@talisman(
#    frame_options='ALLOW-FROM',
#    frame_options_allow_from='https://127.0.0.1:5000/',
#)

def index():
    form = PostForm()
    if form.validate_on_submit():
        flash('Added spellcheck search to database')
        with open('test.txt',"w") as fo:
            fo.write(form.post.data)
        output = check_output(["/app/a.out","test.txt","wordlist.txt"])
        post = Post(body=form.post.data, author=current_user, result=output.decode('utf-8'))
        db.session.add(post)
        db.session.commit()
        return render_template('index.html', title='Home', post=post, result=output.decode('UTF-8'))
    return render_template('index.html', title='Home', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    #output = "anything" 
    if current_user.is_authenticated:
        return redirect(url_for('index'))
        #output = "User already logged in"
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.uname.data).first()
        if user is None or not user.check_password(form.pword.data):
            #output = "Incorrect username or password"
            #return render_template('login.html', title='Sign In', form=form, output=output)
            flash('Incorrect username or password')
            return redirect(url_for('login'))
        if not user.check_password2(form.pword2.data):
            #output = "Two-factor authentication failure"
            #return render_template('login.html', title='Sign In', form=form, output=output)
            flash('Two-factor authentication failure')
            return redirect(url_for('login'))
        flash('Success - User Login Request')
        #output = "Success - User Login Request"
        login_user(user)
        login = Login(user_id = current_user.id)
        db.session.add(login)
        db.session.commit()

        next_page = request.args.get('next')
        if not next_page or urlparse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page) #avoid redirect
        #return render_template('login.html', title='Sign In', form=form, output=output)
    return render_template('login.html', title='Sign In', form=form) #add output=output

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.uname.data)
        user.set_password(form.pword.data)
        user.set_password2(form.pword2.data)
        db.session.add(user)
        db.session.commit()
        flash('Success - User Registration Request')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/logout')
def logout():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    login = Login.query.filter_by(user_id = current_user.id).order_by(Login.id.desc()).first()
    login.logout_timestamp = datetime.utcnow()
    logout_user()
    db.session.commit()

    return redirect(url_for('index'))

@app.route('/history', methods=['GET'])
def history():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    if current_user.username == "admin":
        return redirect(url_for('history_query'))
    else:    
        posts = current_user.spellcheck_posts().all()
        posts_count = current_user.spellcheck_posts().count()
        return render_template("history.html", title='History Page', posts=posts, count=posts_count)

@app.route('/history_query', methods=['GET', 'POST'])
def history_query():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    if current_user.username != "admin":
        return redirect(url_for('history'))
    form = HistoryForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.uname.data).first()
        if user is None:
            flash('No such username')
            return redirect(url_for('history_query'))
        print("UserID:", user.id)
        posts = user.spellcheck_posts().all()
        posts_count = user.spellcheck_posts().count()
        return render_template("history.html", title='History Page', posts=posts, count=posts_count)
    return render_template('history.html', title='History', form=form)

@app.route('/history/query<id>', methods=['GET'])
def query(id):
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    if current_user.username == "admin":
        posts = current_user.spellcheck_posts_all()
    else:
        posts = current_user.spellcheck_posts()
    post = posts.filter_by(id=id).first()
    print(post)
    return render_template('query.html', title='Query', post=post)

@app.route('/login_history', methods=['GET', 'POST'])
def login_history():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    if current_user.username != "admin":
        flash('Not authorized for login history search')
        return redirect(url_for('index'))
    form = LoginHistoryForm()
    if form.validate_on_submit():
        user = User.query.filter_by(id=form.uid.data).first()
        if user is None:
            flash('No such userid')
            return redirect(url_for('login_history'))
        print("UserID:", user.id)
        logins = user.login_logs(user.id).all()
        return render_template("login_history.html", title='Login History Page', logins=logins)
    return render_template('login_history.html', title='Login History', form=form)

