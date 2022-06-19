import json
import os

from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from werkzeug.exceptions import HTTPException

app = Flask(__name__)
CORS(app)


@app.errorhandler(HTTPException)
def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    # start with the correct headers and status code from the error
    response = e.get_response()
    # replace the body with JSON
    response.data = json.dumps(
        {
            "code": e.code,
            "name": e.name,
            "description": e.description,
        }
    )
    response.content_type = "application/json"
    return response


@app.route("/")
def index():
    return {"message": "Hello World!"}


@app.route("/people", methods=["POST", "GET"])
def people():
    if request.method == "GET":
        people = Person.query.all()
        result = []

        for person in people:
            result.append(
                {
                    "id": person.id,
                    "first_name": person.first_name,
                    "contacts": [
                        {"id": contact.id, "contact": contact.contact}
                        for contact in person.contacts
                    ],
                }
            )
        return jsonify(result)
    else:
        person = Person(**request.json)
        db.session.add(person)
        db.session.commit()

        return {"message": "person created"}, 201


@app.route("/contacts", methods=["POST", "GET"])
def contacts():
    if request.method == "GET":
        contacts = Contact.query.all()
        result = []

        for contact in contacts:
            result.append(
                {
                    "id": contact.id,
                    "contact": contact.contact,
                    "person_id": contact.person_id,
                }
            )

        return jsonify(result)
    else:
        contact = Contact(**request.json)
        db.session.add(contact)
        db.session.commit()

        return {"message": "contact created"}, 201


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
print(app.config["SQLALCHEMY_DATABASE_URI"])
db = SQLAlchemy(app)


class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    contacts = db.relationship("Contact", backref="person", lazy=True)


class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    contact = db.Column(db.String())
    person_id = db.Column(
        db.Integer,
        db.ForeignKey("person.id"),
        nullable=False,
    )


# db.create_all()
