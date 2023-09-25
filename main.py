import os
import smtplib

from flask_bootstrap import  Bootstrap5
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField, TelField, TextAreaField
from wtforms.validators import DataRequired

email_to = os.getenv("EMAIL_TO")
email_login = os.getenv("EMAIL_FROM")
email_login_psw = os.getenv("EMAIL_FROM_psw")

app = Flask(__name__)
bootstrap = Bootstrap5(app)
app.config['SECRET_KEY'] = os.getenv("PORTFOLIO_SECRET_KEY")
db = SQLAlchemy()
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///movies.db"

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(25), nullable=False)
    surname = db.Column(db.String(25), nullable=False)
    number = db.Column(db.String(15), nullable=False)
    message = db.Column(db.String(450), nullable=False)


class ContactForm(FlaskForm):
    name = StringField('First Name', validators=[DataRequired()])
    surname = StringField('Last Name', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired()])
    number = TelField('Number', validators=[DataRequired()])
    message = TextAreaField('Message', validators=[DataRequired()])
    submit = SubmitField('SEND')


with app.app_context():
    db.create_all()


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

        con = Contact()
        con.name = name
        con.surname = surname
        con.email = email
        con.number = number
        con.message = message

        db.session.add(con)
        db.session.commit()

        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=email_login, password=email_login_psw)

            connection.sendmail(from_addr=email,
                                to_addrs="rocco.caliandro@toptal.com",
                                msg=message)
        return render_template("index.html", form_complete=True)

    else:
        return render_template("contact.html", form=form)


if __name__ == "__main__":
    app.run(debug=True, port=5003)
