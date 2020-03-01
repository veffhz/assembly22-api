from application import create_app
from application.models import db
from application.schemas import EventSchema, LocationSchema, ParticipantSchema

locations = [
    {
        'id': '1',
        'title': 'Москва',
        'code': 'msc',
    },
    {
        'id': '2',
        'title': 'Санкт-Петербург',
        'code': 'spb',
    },
    {
        'id': '3',
        'title': 'Новосибирск',
        'code': 'nsc',
    },
    {
        'id': '4',
        'title': 'Казань',
        'code': 'kzn',
    },
    {
        'id': '5',
        'title': 'Омск',
        'code': 'omsk',
    },
    {
        'id': '6',
        'title': 'Сочи',
        'code': 'soch',
    },
    {
        'id': '7',
        'title': 'Екатеринбург',
        'code': 'ekb',
    },

]

events = [
    {
        'id': '1',
        'title': 'Python конференция',
        'description': 'Достижения народного хозяйства',
        'date': '2021-01-02',
        'time': '11:00',
        'type': 'workshop',
        'category': 'python',
        'location_id': 1,
        'address': 'улица Правды, дом 15',
        'seats': '90',
    },
    {
        'id': '2',
        'title': 'Java конференция',
        'description': 'Достижения народного хозяйства',
        'date': '2020-03-02',
        'time': '9:00',
        'type': 'workshop',
        'category': 'java',
        'location_id': 2,
        'address': 'улица Правды, дом 15',
        'seats': '80',
    },
    {
        'id': '3',
        'title': 'Go конференция',
        'description': 'Достижения народного хозяйства',
        'date': '2020-03-02',
        'time': '15:00',
        'type': 'hackathon',
        'category': 'go',
        'location_id': 7,
        'address': 'улица Химмаш, дом 1',
        'seats': '8',
    },
    {
        'id': '4',
        'title': 'ML конференция',
        'description': 'Достижения народного хозяйства',
        'date': '2020-08-08',
        'time': '12:00',
        'type': 'hackathon',
        'category': 'ml',
        'location_id': 3,
        'address': 'Академгородок',
        'seats': '999',
    },
    {
        'id': '5',
        'title': 'Управление проектами',
        'description': 'Достижения народного хозяйства',
        'date': '2021-04-05',
        'time': '13:00',
        'type': 'game',
        'category': 'pm',
        'location_id': 3,
        'address': 'Академгородок',
        'seats': '3',
    },

]

participants = [
    {
        'id': "1",
        'name': "Foo Bar",
        'email': "foo@bar.com",
        'password': "123456",
        'picture': "pic1.png",
        'location': "msc, len st 5",
        'about': "just me",
        'events': [1, 2]
    },
    {
        'id': "2",
        'name': "Num Two",
        'email': "num@bar.com",
        'password': "123456",
        'picture': "pic2.png",
        'location': "spb, len st 5",
        'about': "just me",
        'events': [2, 3]
    },
    {
        'id': "3",
        'name': "Num n",
        'email': "num3@bar.com",
        'password': "123456",
        'picture': "pic3.png",
        'location': "ekb, len st 5",
        'about': "just me",
        'events': [3, 4]
    },
    {
        'id': "4",
        'name': "Foo Bar 4",
        'email': "foo4@bar.com",
        'password': "123456",
        'picture': "pic4.png",
        'location': "msc, len st 5",
        'about': "just me",
        'events': [4, 5]
    },
    {
        'id': "5",
        'name': "Num Two 5",
        'email': "num5@bar.com",
        'password': "123456",
        'picture': "pic5.png",
        'location': "spb, len st 5",
        'about': "just me",
        'events': [1, 2, 3]
    },
    {
        'id': "6",
        'name': "Num n #6",
        'email': "num6@bar.com",
        'password': "123456",
        'picture': "pic6.png",
        'location': "ekb, len st 5",
        'about': "just me",
        'events': [1, 2, 3, 4, 5]
    },
]


def run():
    app = create_app()
    app.app_context().push()

    location_schema = LocationSchema()
    event_schema = EventSchema()
    participant_schema = ParticipantSchema()

    for location in locations:
        loc = location_schema.load(location)
        db.session.add(loc)

    db.session.commit()

    for event in events:
        evt = event_schema.load(event)
        db.session.add(evt)

    db.session.commit()

    for participant in participants:
        ps = participant_schema.load(participant)
        db.session.add(ps)

    db.session.commit()


if __name__ == "__main__":
    run()
