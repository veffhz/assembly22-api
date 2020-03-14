from flask import jsonify
from sqlalchemy import and_
from flask_apispec import marshal_with
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound
from flask_jwt_extended import jwt_required, get_jwt_identity

from application import app
from application.models import db, Event, Participant, Enrollment


@app.route('/enrollments/<int:event_id>/', methods=['POST'])
@jwt_required
def post_enrollments(event_id):

    event = Event.query.filter_by(id=event_id).first()

    if not event or event.seats <= len(event.enrollments):
        return jsonify({"status": "error"})

    email = get_jwt_identity()
    participant = Participant.query.filter_by(email=email).first()

    enrollment = Enrollment(event=event, participant=participant)

    try:
        db.session.add(enrollment)
        db.session.commit()
        return jsonify({"status": "success"}), 201
    except IntegrityError as e:
        app.logger.error(e)
        return jsonify({"status": "error"}), 400


@app.route('/enrollments/<int:event_id>/', methods=['DELETE'])
@jwt_required
@marshal_with(None, code=204)
def delete_enrollment(event_id):

    event = Event.query.filter_by(id=event_id).first()

    if not event or len(event.enrollments) < 1:
        return jsonify({"status": "error"})

    email = get_jwt_identity()

    try:
        enrollment = Enrollment.query.join(Participant).filter(
            and_(Enrollment.event_id == event_id, Participant.email == email)).one()

        db.session.delete(enrollment)
        db.session.commit()
        return None
    except (IntegrityError, NoResultFound) as e:
        app.logger.error(e)
        return jsonify({"status": "error"}), 400
