from flask_jwt_extended import jwt_required
from flask_apispec import marshal_with, doc
from flask import jsonify, request, make_response

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
@doc(
    description='Get all events',
    params={
        'event_type': {
            'description': 'Type param for event, like: <b>workshop</b>',
            'in': 'query',
            'enum': [evt for evt, _ in EventType],
            'type': 'string'
        },
        'location': {
            'description': 'Location param for event, like: <b>msc</b>',
            'in': 'query',
            'type': 'string'
        }
    })
@marshal_with(EventSchema(many=True))
def get_events():
    event_type = request.args.get('event_type')
    location = request.args.get('location')

    query = Event.query

    if event_type:
        query = query.filter(Event.type == event_type)
    if location:
        query = query.join(Location).filter(Location.code == location)

    return query.all()


@app.route('/profile/<int:uid>/', methods=['GET'])
@doc(
    description='Token access',
    params={
        'Authorization': {
            'description': 'Authorization HTTP header with JWT access token, like: <b>Bearer token<b>',
            'in': 'header',
            'type': 'string',
            'required': True
        }
    })
@jwt_required
@marshal_with(ParticipantSchema(), code=200)
def get_profile(uid):
    participant = Participant.query.filter_by(id=uid).first()

    if participant:
        return participant
    else:
        return make_response(
            jsonify({"status": "error"}), 404
        )
