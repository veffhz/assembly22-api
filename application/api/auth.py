from flask import jsonify, request
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import create_access_token

from application import app
from application.models import db, Participant
from application.schemas import ParticipantSchema


@app.route('/auth/', methods=['POST'])
def post_auth():
    data = request.json

    email = data.get("email")
    password = data.get("password")

    participant = Participant.query.filter_by(email=email).first()

    if participant and participant.check_password(password):
        access_token = create_access_token(identity=email)
        participant_schema = ParticipantSchema()
        return jsonify({
            'participant': participant_schema.dump(participant),
            'key': access_token
        }), 200
    else:
        return jsonify({"status": "error"}), 401


@app.route('/register/', methods=['POST'])
def post_register():
    data = request.json

    try:
        participant_schema = ParticipantSchema()
        participant = participant_schema.load(data)
        db.session.add(participant)
        db.session.commit()
        return jsonify({
            'participant': participant_schema.dump(participant),
            'password': data.get("password")
        }), 201
    except (IntegrityError, ValidationError) as e:
        app.logger.error(e)
        return jsonify({"status": "error"}), 400
