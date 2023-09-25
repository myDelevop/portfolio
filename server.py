import os
from flask_bootstrap import Bootstrap
from flask import Flask, render_template, request, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField, TelField, TextAreaField
from wtforms.validators import DataRequired

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = os.environ.get("PORTFOLIO_SECRET_KEY")


class ContactForm(FlaskForm):
    name = StringField('First Name', validators=[DataRequired()])
    surname = StringField('Last Name', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired()])
    number = TelField('Number', validators=[DataRequired()])
    message = TextAreaField('Message', validators=[DataRequired()])
    submit = SubmitField('SEND')


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/about')
def about():
    return "About"


@app.route('/contact', methods=["GET", "POST"])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        name = request.form.get("name")
        surname = request.form.get("surname")
        email = request.form.get("email")
        number = request.form.get("number")
        message = request.form.get("message")

        return render_template("index.html", form_complete=True)

    else:
        return render_template("contact.html", form=form)


if __name__ == "__main__":
    app.run(debug=True, port=5003)
