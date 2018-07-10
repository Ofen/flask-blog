from app import app
from flask import render_template, flash, redirect, url_for, session, Markup, abort, request
from werkzeug.security import check_password_hash, generate_password_hash
from forms import *
import sqlite3
from functools import wraps
from datetime import datetime
import os

def get_current_datetime():
    return datetime.now().strftime("%d.%m.%Y %H:%M:%S")

def get_db():
    APP_FOLDER = os.path.dirname(os.path.abspath(__file__))
    db = sqlite3.connect(os.path.join(APP_FOLDER, "database.db"))
    db.row_factory = sqlite3.Row
    return db

def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if session.get('user_id') is None:
            return abort(404)
        return func(*args, **kwargs)
    return wrapper

def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if session.get('role_id') != 2:
            return abort(404)
        return func(*args, **kwargs)
    return wrapper

# @app.before_app_request
# def load_logged_in_user():
#     user_id = session['user_id']

@app.route('/')
def home():
    db = get_db()
    posts = db.execute("SELECT id, created, title, content FROM posts").fetchall()
    return render_template('index.html', posts=reversed(posts))

@app.route('/sign_in', methods=['GET', 'POST'])
def sign_in():
    form = SignInForm()
    if form.validate_on_submit():
        db = get_db()
        if db.execute("SELECT username FROM users WHERE username=?", (form.username.data,)).fetchone():
            db.close()
            flash(Markup('User <strong>%s</strong> already exists!' % form.username.data), "alert-danger")
            return redirect(url_for('sign_in'))
        else:
            user_role = db.execute("SELECT * FROM roles WHERE role='user'").fetchone()
            db.execute("INSERT INTO users(username, password, role_id) VALUES(?, ?, ?)", (form.username.data, generate_password_hash(form.password.data), user_role['id']))
            db.commit()
            db.close()
            flash(Markup('User <strong>%s</strong> added to database!' % form.username.data), "alert-success")
            return redirect(url_for('home'))
    return render_template('sign_in.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db = get_db()
        user = db.execute("SELECT * FROM users WHERE username=?", (form.username.data,)).fetchone()

        if user is None:
            flash('Incorrect login or password', "alert-danger")
            return redirect(url_for('login'))
        elif not check_password_hash(user['password'], form.password.data):
            flash('Incorrect login or password', "alert-danger")
            return redirect(url_for('login'))
        else:
            session.clear()
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['role_id'] = user['role_id']
            return redirect(url_for('home'))

    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    session.clear()
    return redirect(url_for('home'))

@app.route('/new_post', methods=['GET', 'POST'])
@login_required
def new_post():
    form = NewPostForm()
    if form.validate_on_submit():
        db = get_db()
        db.execute("INSERT INTO posts(user_id, created, title, content) VALUES(?, ?, ?, ?)", (session['user_id'], get_current_datetime(), form.title.data, form.content.data))
        db.commit()
        db.close()
        flash('New post added!', "alert-success")
        return redirect(url_for('home'))
    return render_template('new_post.html', form=form)

@app.route('/delete_post', methods=['POST'])
@admin_required
def delete_post():
    post_id = request.form.get('post-id')
    if post_id is not None:
        db = get_db()
        db.execute("DELETE FROM posts WHERE id=?", (post_id,))
        db.commit()
        flash("Post deleted!", "alert-success")
        return redirect(url_for('home'))

@app.route('/profile/<username>')
@login_required
def profile(username):
    return username

@app.errorhandler(403)
def page_not_found(e):
    return render_template("error.html", error=e), 403

@app.errorhandler(404)
def page_not_found(e):
    return render_template("error.html", error=e), 404

@app.errorhandler(405)
def page_not_found(e):
    return render_template("error.html", error=e), 405

@app.errorhandler(410)
def page_not_found(e):
    return render_template("error.html", error=e), 410

@app.errorhandler(500)
def page_not_found(e):
    return render_template("error.html", error=e), 500