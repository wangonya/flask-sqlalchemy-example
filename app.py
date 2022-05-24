import os

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

@app.route("/")
def index():
    return {"message": "Hello World!"}

@app.route("/users/create", methods=["POST"])
def create_user():
    person = Person(**request.json)
    db.session.add(person)
    db.session.commit()
    return {"message": "User created"}

@app.route("/contacts/create/", methods=["POST"])
def create_contact():
    return {"message": "Contact created"}


@app.route("/contacts/")
def get_all_contacts():
    return {"message": "Contacts queried"}

@app.route("/users/")
def get_all_users():
    users = Person.query.all()
    print(users)
    return {"message": "Users queried"}


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
    contacts = db.relationship('Contact', backref='person', lazy=True)


class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    contact = db.Column(db.String())
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'),
        nullable=False)

db.create_all()
