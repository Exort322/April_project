from flask import Flask, render_template, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField, TextAreaField, SelectField
from wtforms.fields.simple import BooleanField
from wtforms.validators import DataRequired, Email, EqualTo
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'silly_joke_secret_key'


class RegistrationForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired(), EqualTo('password')])
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


@app.route('/', methods=['GET', 'POST'])
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash('Регистрация прошла успешно!', 'success')
        return redirect(url_for('welcome'))
    return render_template('registration.html', form=form)


@app.route('/welcome')
def welcome():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Вы успешно вошли в систему!', 'success')
        return redirect(url_for('welcome'))
    return render_template('login.html', form=form)


@app.route('/profile')
def profile():
    user_data = {
        'username': 'test',
        'email': 'test@test',
        'registration_date': datetime(2025, 1, 1),
        'jokes_count': 5
    }
    return render_template('profile.html', user=user_data)


@app.route('/create_joke', methods=['GET', 'POST'])
def create_joke():
    form = JokeForm()
    if form.validate_on_submit():
        flash('Шутка добавлена успешно!', 'success')
        return redirect(url_for('welcome'))
    return render_template('create_joke.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
