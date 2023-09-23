from flask import Flask, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField
from wtforms.validators import DataRequired, Email
from datetime import datetime

num = 1
class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    email = EmailField('What is your UofT Email address?', validators=[DataRequired(), Email()])
    submit = SubmitField('Submit')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'abi#83jvmf93'
app.config['SESSION_PERMANENT'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = 3600     # reset session every hour
bootstrap = Bootstrap(app)
moment = Moment(app)

"""
@app.route('/')
def index():
    return render_template('user.html', name='Ardavan',
                           current_time=datetime.utcnow())
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    session['submitted_email'] = form.email.data
    if form.validate_on_submit():
        old_name = session.get('name')
        old_email = session.get('email')
        if old_name is not None and old_name != form.name.data:     # check if the name has changed
            flash('Looks like you have changed your name!')
        if old_email is not None and old_email != form.email.data:     # check if the email has changed
            flash('Looks like you have changed your email!')
        session['name'] = form.name.data
        session['email'] = form.email.data
        return redirect(url_for('index'))
    return render_template('index.html', form=form, name=session.get('name'), email=session.get('email'))

if __name__ == '__main__':
    app.run()
