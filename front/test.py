import sys
from pathlib import Path
from flask import Flask, render_template, redirect, url_for, flash, session, request, jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField, TextAreaField, SelectField
from wtforms.fields.simple import BooleanField
from wtforms.validators import DataRequired, Email, EqualTo
from werkzeug.security import generate_password_hash, check_password_hash


sys.path.append(str(Path(__file__).parent.parent / "back"))

from database import (
    add_user, get_user_by_username, update_user_activity,
    add_joke, get_random_joke, rate_joke, get_popular_jokes,
    get_user_jokes_count
)

app = Flask(__name__, template_folder='templates')
app.secret_key = 'silly_joke_secret_key'


# Формы
class RegistrationForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль',
                                   validators=[DataRequired(), EqualTo('password')])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Зарегистрироваться')


class LoginForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class JokeForm(FlaskForm):
    joke_text = TextAreaField('Текст шутки', validators=[DataRequired()])
    joke_category = SelectField('Тематика шутки', choices=[
        ('анекдоты', 'Анекдоты'),
        ('шутки', 'Шутки'),
        ('юмор', 'Юмор')
    ], validators=[DataRequired()])
    submit = SubmitField('Добавить шутку')


# Роуты
@app.route('/', methods=['GET', 'POST'])
@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'user_id' in session:
        return redirect(url_for('welcome'))

    form = RegistrationForm()
    if form.validate_on_submit():
        password_hash = generate_password_hash(form.password.data)
        user_id = add_user(form.username.data, form.email.data, password_hash)
        if user_id == -1:
            flash('Пользователь с таким именем или email уже существует!', 'danger')
        else:
            flash('Регистрация прошла успешно!', 'success')
            session['user_id'] = user_id
            session['username'] = form.username.data
            return redirect(url_for('welcome'))
    return render_template('registration.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('welcome'))

    form = LoginForm()
    if form.validate_on_submit():
        user = get_user_by_username(form.username.data)
        if user and check_password_hash(user['password_hash'], form.password.data):
            flash('Вы успешно вошли в систему!', 'success')
            session['user_id'] = user['id']
            session['username'] = user['username']
            update_user_activity(user['id'])
            return redirect(url_for('welcome'))
        else:
            flash('Неверное имя пользователя или пароль', 'danger')
    return render_template('registration.html', form=form)


@app.route('/logout')
def logout():
    session.clear()
    flash('Вы успешно вышли из системы', 'success')
    return redirect(url_for('login'))


@app.route('/welcome')
def welcome():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    update_user_activity(session['user_id'])
    random_joke = get_random_joke(session.get('user_id'))
    popular_jokes = get_popular_jokes(3)

    return render_template('index.html',
                           random_joke=random_joke,
                           popular_jokes=popular_jokes,
                           username=session.get('username'))


@app.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    update_user_activity(session['user_id'])
    jokes_count = get_user_jokes_count(session['user_id'])

    return render_template('profile.html',
                           user={
                               'username': session['username'],
                               'jokes_count': jokes_count
                           })


@app.route('/create_joke', methods=['GET', 'POST'])
def create_joke():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    form = JokeForm()
    if form.validate_on_submit():
        print(f"Добавляем шутку: {form.joke_text.data}, категория: {form.joke_category.data}")

        joke_id = add_joke(
            user_id=session['user_id'],
            text=form.joke_text.data,
            category=form.joke_category.data
        )

        if joke_id:
            flash('Шутка успешно добавлена!', 'success')
            return redirect(url_for('welcome'))

    return render_template('create_joke.html', form=form)


@app.route('/rate_joke', methods=['POST'])
def rate_joke():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    joke_id = request.json.get('joke_id')
    rating = request.json.get('rating')

    if joke_id and rating in (1, -1):
        success = rate_joke(session['user_id'], joke_id, rating)
        return jsonify({'success': success})
    return jsonify({'success': False})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)