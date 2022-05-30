import os

from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/people/add", methods=["POST", "GET"])
def create_person():
    if request.method == "GET":
        return render_template("create-person.html")

    person = Person(**request.form)
    db.session.add(person)
    db.session.commit()

    return jsonify({"redirect": "/people"})


@app.route("/people/")
def get_all_people():
    people = Person.query.all()
    return render_template("people.html", people=people)


@app.route("/contacts/add/", methods=["POST", "GET"])
def create_contact():
    if request.method == "GET":
        people = Person.query.all()
        return render_template("create-contact.html", people=people)

    contact = Contact(**request.form)
    db.session.add(contact)
    db.session.commit()

    return jsonify({"redirect": "/contacts"})


@app.route("/contacts/")
def get_all_contacts():
    contacts = Contact.query.all()
    people = Person.query.all()
    return render_template("contacts.html", contacts=contacts, people=people)


# get single contact

# update contact

# delete contact


##########
# models #
##########

DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_SERVER = os.getenv("DB_SERVER")
DB_NAME = os.getenv("DB_NAME")

app.config[
    "SQLALCHEMY_DATABASE_URI"
] = f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_SERVER}:5432/{DB_NAME}"
db = SQLAlchemy(app)


class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    contacts = db.relationship("Contact", backref="person", lazy=True)

    def __repr__(self):
        return self.first_name


class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    contact = db.Column(db.String())
    person_id = db.Column(db.Integer, db.ForeignKey("person.id"), nullable=False)

    def __repr__(self):
        return self.contact


# db.create_all()
