from marshmallow import Schema, fields, post_load

from application.models import EventType, CategoryType, Location, Event, Participant


class EventSchema(Schema):
    id = fields.Integer()
    title = fields.String(required=True)
    description = fields.String(required=True)
    date = fields.Date(required=True)
    time = fields.Time(required=True)
    type = fields.Method("get_type", deserialize="load_type")
    category = fields.Method("get_category", deserialize="load_category")
    location_id = fields.Integer(required=True, load_only=True)
    location = fields.Nested('LocationSchema', required=True, dump_only=True)
    address = fields.String(required=True)
    seats = fields.Integer(required=True)
    enrollments = fields.List(fields.Nested('EnrollmentSchema', only=('id', 'datetime')))
    participants = fields.List(fields.Nested('ParticipantSchema', only=('name',)))

    @post_load()
    def make_event(self, data, **kwargs):
        return Event(**data)

    @staticmethod
    def load_type(key):
        if key in dict(EventType):
            return key

    @staticmethod
    def get_type(obj):
        return obj.type.code

    @staticmethod
    def load_category(key):
        if key in dict(CategoryType):
            return key

    @staticmethod
    def get_category(obj):
        return obj.category.code


class ParticipantSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True)
    email = fields.Email(required=True)
    password = fields.String(load_only=True, required=True)
    picture = fields.String()
    location = fields.String(required=True)
    about = fields.String()
    enrollments = fields.List(fields.Nested('EnrollmentSchema', only=("id", )), dump_only=True)
    events = fields.Method("get_events", exclude=('participants',), deserialize="load_events")

    @post_load()
    def make_participant(self, data, **kwargs):
        return Participant(**data)

    @staticmethod
    def load_events(event_ids):
        return Event.query.filter(Event.id.in_(event_ids)).all()

    @staticmethod
    def get_events(obj):
        return [e.id for e in obj.events]


class EnrollmentSchema(Schema):
    id = fields.Integer()
    event = fields.Nested('EnrollmentSchema', required=True)
    participant = fields.Nested('ParticipantSchema', required=True)
    datetime = fields.DateTime(required=True)


class LocationSchema(Schema):
    id = fields.Integer()
    title = fields.String(required=True)
    code = fields.String(required=True)
    events = fields.List(fields.Nested('EventSchema', only=("id", )))

    @post_load
    def make_location(self, data, **kwargs):
        return Location(**data)
