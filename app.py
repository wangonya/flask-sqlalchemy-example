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


# delete person
@app.route("/people/<int:person_id>", methods=["DELETE"])
def delete_person(person_id):
    person = Person.query.get(person_id)
    db.session.delete(person)
    db.session.commit()
    return {"message": "person deleted"}


@app.route("/people/<int:person_id>", methods=["PATCH"])
def update_person(person_id):
    person = Person.query.get(person_id)
    person.first_name = request.json.get("first_name")
    db.session.commit()
    return {"message": "person updated", "first_name": person.first_name}


# get single contact


@app.route("/contacts/<int:contact_id>", methods=["DELETE"])
def delete_contact(contact_id):
    contact = Contact.query.get(contact_id)
    db.session.delete(contact)
    db.session.commit()
    return {"message": "contact deleted"}


@app.route("/contacts/<int:contact_id>", methods=["PATCH"])
def update_contact(contact_id):
    contact = Contact.query.get(contact_id)
    contact.contact = request.json.get("contact")
    db.session.commit()
    return {"message": "contact updated"}


# search
@app.route("/people/search")
def search_people():
    search_term = request.args.get("first_name")
    people = Person.query.filter(Person.first_name.ilike(f"%{search_term}%")).all()

    if not people:
        return {}, 404

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


@app.route("/contacts/search", methods=["POST"])
def search_contacts():
    search_term = request.get_json().get("contact")
    contacts = Contact.query.filter(Contact.contact.ilike(f"%{search_term}%")).all()
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


##########
# models #
##########

DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_SERVER = os.getenv("DB_SERVER")
DB_NAME = os.getenv("DB_NAME")

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://kelvin:@localhost:5432/contacts"
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
