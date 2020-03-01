from flask import jsonify, request
from flask_jwt_extended import jwt_required

from application import app
from application.models import Location, Event, Participant
from application.schemas import LocationSchema, EventSchema, ParticipantSchema


@app.route('/locations/', methods=['GET'])
def get_locations():
    locations = Location.query.all()
    locations_schema = LocationSchema(many=True)
    return jsonify(locations_schema.dump(locations))


@app.route('/events/', methods=['GET'])
def get_events():
    eventtype = request.args.get('eventtype')
    location = request.args.get('location')

    query = Event.query

    if eventtype:
        query = query.filter(Event.type == eventtype)
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
