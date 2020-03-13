from webargs import fields
from flask import jsonify, request
from flask_apispec import marshal_with, use_kwargs
from flask_jwt_extended import jwt_required

from application import app
from application.models import Location, Event, Participant, EventType
from application.schemas import LocationSchema, EventSchema, ParticipantSchema


@app.route('/locations/', methods=['GET'])
@marshal_with(LocationSchema(many=True))
def get_locations():
    locations = Location.query.all()
    locations_schema = LocationSchema(many=True)
    return jsonify(locations_schema.dump(locations))


@app.route('/events/', methods=['GET'])
@use_kwargs({'event_type': fields.Str(enum=[evt for evt, _ in EventType])}, locations=('query',))
@marshal_with(EventSchema(many=True))
def get_events(**kwargs):
    event_type = request.args.get('event_type')
    location = request.args.get('location')

    query = Event.query

    if event_type:
        query = query.filter(Event.type == event_type)
    if location:
        query = query.join(Location).filter(Location.code == location)

    events = query.all()
    events_schema = EventSchema(many=True)
    return jsonify(events_schema.dump(events))


@app.route('/profile/<int:uid>/', methods=['GET'])
@jwt_required
def get_profile(uid):
    participant = Participant.query.filter_by(id=uid).first()

    if participant:
        participant_schema = ParticipantSchema()
        return jsonify(participant_schema.dump(participant)), 200
    else:
        return jsonify({"status": "error"}), 404
