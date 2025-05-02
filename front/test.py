from flask import Flask, render_template, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, EmailField
from wtforms.fields.simple import BooleanField
from wtforms.validators import DataRequired, Email, EqualTo

app = Flask(__name__)
app.secret_key = 'silly_joke_secret_key'


class RegistrationForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired(), EqualTo('password')])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Зарегистрироваться')


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


@app.route('/profile')
def profile():
    user_data = {
        'username': 'example_user',
        'email': 'user@example.com'
    }
    return render_template('profile.html', user=user_data)



if __name__ == '__main__':
    app.run(debug=True)
