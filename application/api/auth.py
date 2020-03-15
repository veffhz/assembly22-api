from flask_apispec import use_kwargs
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from flask import jsonify, request, make_response
from flask_jwt_extended import create_access_token

from application import app
from application.models import db, Participant
from application.schemas import ParticipantSchema


@app.route('/auth/', methods=['POST'])
@use_kwargs(ParticipantSchema(only=('email', 'password')))
def post_auth(*args):
    data = request.json

    email = data.get("email", None)
    password = data.get("password", None)

    participant = Participant.query.filter_by(email=email).first()

    if participant and participant.check_password(password):
        access_token = create_access_token(identity=email)
        participant_schema = ParticipantSchema()
        return make_response(jsonify({
            'participant': participant_schema.dump(participant),
            'key': access_token
        }), 200)
    else:
        return make_response(
            jsonify({"status": "error"}), 401
        )


@app.route('/register/', methods=['POST'])
@use_kwargs(ParticipantSchema)
def post_register(*args):
    data = request.json

    try:
        participant_schema = ParticipantSchema()
        participant = participant_schema.load(data)
        db.session.add(participant)
        db.session.commit()
        return make_response(jsonify({
            'participant': participant_schema.dump(participant),
            'password': data.get("password")
        }), 201)
    except (IntegrityError, ValidationError) as e:
        app.logger.error(e)
        return make_response(
            jsonify({"status": "error"}), 400
        )
