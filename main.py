import os
import smtplib
import ssl
import datetime
from flask_bootstrap import Bootstrap5
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField, TelField, TextAreaField, DateTimeLocalField
from wtforms.validators import DataRequired

email_to = os.getenv("EMAIL_TO")
email_login = os.getenv("EMAIL_FROM")
email_login_psw = os.getenv("EMAIL_FROM_psw")

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("PORTFOLIO_SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DB_URI_PORTFOLIO")

bootstrap = Bootstrap5(app)
db = SQLAlchemy()
db.init_app(app)


class Contact(db.Model):
    __tablename__ = "contacts"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(25), nullable=False)
    surname = db.Column(db.String(25), nullable=False)
    number = db.Column(db.String(15), nullable=False)
    message = db.Column(db.String(450), nullable=False)
    dt = db.Column(db.DateTime, nullable=False)


class ContactForm(FlaskForm):
    name = StringField('Name', render_kw={"placeholder": "Name"}, validators=[DataRequired()])
    surname = StringField('Last Name', render_kw={"placeholder": "Last Name"}, validators=[DataRequired()])
    email = EmailField('Email', render_kw={"placeholder": "Email"}, validators=[DataRequired()])
    number = TelField('Number', render_kw={"placeholder": "Number"}, validators=[DataRequired()])
    message = TextAreaField('Message', render_kw={"placeholder": "Message"}, validators=[DataRequired()])
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
        con.dt = datetime.datetime.now()
        app.debug = True
        db.session.add(con)
        db.session.commit()

        smtp_server = "smtp.gmail.com"
        port = 587  # For starttls
        sender_email = "rockdesires@gmail.com"
        password = email_login_psw

        # Create a secure SSL context
        context = ssl.create_default_context()

        # Try to log in to server and send email
        try:
            server = smtplib.SMTP(smtp_server, port)
            server.ehlo()  # Can be omitted
            server.starttls(context=context)  # Secure the connection
            server.ehlo()  # Can be omitted
            server.login(sender_email, password)
            # TODO: Send email here
        except Exception as e:
            # Print any error messages to stdout
            return render_template("index.html", form_complete=0)
        finally:
            server.quit()


        app.debug = False
        # try:
        #with smtplib.SMTP("smtp.gmail.com") as connection:
            #print("CIZO")
            # connection.starttls()
            # connection.login(user=email_login, password=email_login_psw)
            # connection.sendmail(from_addr=email_login,
            #                     to_addrs="rocco.caliandro@toptal.com",
            #                     msg=f"Subject: Message from {name} {surname} with email: {email}\n\n"
            #                         f"You've received a message from {name} {surname} with email: {email}"
            #                         f"at {con.dt}  o'clock.\nThe contact number is: {number}.\n\n\n"
            #                         f"Let's think to the content of the message:\n\n\n\n {message}\n\n"
            #                         f"by: {email}")

        # except Exception as e:
        # return render_template("index.html", form_complete=0)

        return render_template("index.html", form_complete=1)
    else:
        return render_template("contact.html", form=form)


if __name__ == "__main__":
    app.run(debug=True, port=5003)
