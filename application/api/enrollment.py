from sqlalchemy import and_
from flask_apispec import doc
from flask import jsonify, make_response
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound
from flask_jwt_extended import jwt_required, get_jwt_identity

from application import app
from application.models import db, Event, Participant, Enrollment


@app.route('/enrollments/<int:event_id>/', methods=['POST'])
@doc(
    description='Enroll to event',
    params={
        'Authorization': {
            'description': 'Authorization HTTP header with JWT access token, like: <b>Bearer token<b>',
            'in': 'header',
            'type': 'string',
            'required': True
        },
        'event_id': {
            'description': 'Event id param for event, like: <b>5</b>',
            'in': 'path',
            'type': 'integer'
        },
    })
@jwt_required
def post_enrollments(event_id):

    event = Event.query.filter_by(id=event_id).first()

    if not event or event.seats <= len(event.enrollments):
        return make_response(jsonify({"status": "error"}), 400)

    email = get_jwt_identity()
    participant = Participant.query.filter_by(email=email).first()

    enrollment = Enrollment(event=event, participant=participant)

    try:
        db.session.add(enrollment)
        db.session.commit()
        return make_response(
            jsonify({"status": "success"}), 201
        )
    except IntegrityError as e:
        app.logger.error(e)
        return make_response(
            jsonify({"status": "error"}), 400
        )


@app.route('/enrollments/<int:event_id>/', methods=['DELETE'])
@doc(
    description='Unsubscribe from event',
    params={
        'Authorization': {
            'description': 'Authorization HTTP header with JWT access token, like: <b>Bearer token<b>',
            'in': 'header',
            'type': 'string',
            'required': True
        },
        'event_id': {
            'description': 'Event id param for event, like: <b>5</b>',
            'in': 'path',
            'type': 'integer'
        },
    })
@jwt_required
def delete_enrollment(event_id):

    event = Event.query.filter_by(id=event_id).first()

    if not event or len(event.enrollments) < 1:
        return make_response(jsonify({"status": "error"}), 400)

    email = get_jwt_identity()

    try:
        enrollment = Enrollment.query.join(Participant).filter(
            and_(Enrollment.event_id == event_id, Participant.email == email)).one()

        db.session.delete(enrollment)
        db.session.commit()
        return make_response(
            jsonify({}), 204
        )
    except (IntegrityError, NoResultFound) as e:
        app.logger.error(e)
        return make_response(
            jsonify({"status": "error"}), 400
        )
