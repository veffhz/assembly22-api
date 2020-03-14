from datetime import datetime

from sqlalchemy import event
from sqlalchemy.orm.base import NO_VALUE
from sqlalchemy_utils import ChoiceType
from werkzeug.security import generate_password_hash, check_password_hash

from application.extensions import db

EventType = [
    ('hackathon', 'Хакатон'),
    ('workshop', 'Воркшоп'),
    ('game', 'Игра'),
]

CategoryType = [
    ('python', 'Python'),
    ('java', 'Java'),
    ('go', 'Go'),
    ('ml', 'ML'),
    ('pm', 'Управление проектами'),
]


class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(80), nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    type = db.Column(ChoiceType(EventType), nullable=False)
    category = db.Column(ChoiceType(CategoryType), nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey("locations.id"))
    location = db.relationship("Location", back_populates="events", lazy='joined')
    address = db.Column(db.String(80), nullable=False)
    seats = db.Column(db.Integer)

    enrollments = db.relationship("Enrollment", back_populates="event", lazy='joined')

    participants = db.relationship(
        'Participant', secondary='enrollments', back_populates='events', lazy='joined'
    )

    def __str__(self):
        return f'{self.title}'


class Participant(db.Model):
    __tablename__ = 'participants'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    picture = db.Column(db.String(80))
    location = db.Column(db.String(80), nullable=False)
    about = db.Column(db.String(180))
    enrollments = db.relationship("Enrollment", back_populates="participant", lazy='joined')

    events = db.relationship(
        'Event', secondary='enrollments', back_populates='participants', lazy='joined'
    )

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, str(password))

    def __str__(self):
        return f'{self.name}'


@event.listens_for(Participant.password, 'set', retval=True)
def hash_user_password(target, value, old_value, initiator):
    if value != old_value:
        return generate_password_hash(value)
    else:
        return old_value


class Enrollment(db.Model):
    __tablename__ = 'enrollments'
    __table_args__ = (
        db.UniqueConstraint('event_id', 'participant_id', name='event-participant-constraint'),
    )

    id = db.Column(db.Integer, primary_key=True)

    event_id = db.Column(db.Integer, db.ForeignKey("events.id"))
    event = db.relationship("Event", back_populates="enrollments", lazy='joined')

    participant_id = db.Column(db.Integer, db.ForeignKey("participants.id"))
    participant = db.relationship("Participant", back_populates="enrollments", lazy='joined')

    datetime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __str__(self):
        return f'{self.id}'


class Location(db.Model):
    __tablename__ = 'locations'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True, nullable=False)
    code = db.Column(db.String(8), unique=True, nullable=False)
    events = db.relationship("Event", back_populates="location", lazy='joined')

    def __str__(self):
        return f'{self.title}'
