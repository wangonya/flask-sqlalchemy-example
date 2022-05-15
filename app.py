import os

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


@app.route("/contacts/create/", methods=["POST"])
def create_contact():
    person = Person(**request.json)
    db.session.add(person)
    db.session.commit()
    return {"message": "User created"}


@app.route("/contacts/")
def get_all_contacts():
    all_contacts = Person.query.all()
    print(all_contacts)
    return {"contacts": 1}


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

    def __repr__(self):
        return self.first_name


class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)


db.create_all()
