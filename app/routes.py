from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app import app, db
from app.forms import LoginForm, RegistrationForm
from app.models import User, Todo
from datetime import date

@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html', User=current_user)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/todo2", methods=['GET'])
def todo():
    todo_list = Todo.query.filter_by(user_id=current_user.id)
    return render_template("todo2.html", todo_list=todo_list)
    
@app.route("/add", methods=["POST"])
def add():
    title = request.form.get("title")
    new_todo = Todo(title=title, user_id=current_user.id, complete=False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("todo"))


@app.route("/update/<int:todo_id>")
def update(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for("todo"))


@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("todo"))

@app.route("/star/<int:todo_id>")
def star(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    todo.star = not todo.star
    db.session.commit()
    return redirect(url_for("todo"))

    
@app.route('/stats')
def stats():
    todo_all = Todo.query.count()
    todo_completed = Todo.query.filter_by(complete=1).count()
    todo_notcompleted = Todo.query.filter_by(complete=0).count()
    print(todo_all)
    print(todo_completed)
    return render_template('stats.html', todo_all=todo_all, todo_completed=todo_completed, todo_notcompleted=todo_notcompleted)


@app.route("/todo2/filter", methods=['GET'])
def filter():
    todo_list = Todo.query.filter_by(star=1) 
    return render_template("todo2.html", todo_list=todo_list)