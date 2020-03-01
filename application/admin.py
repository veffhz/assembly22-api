from flask_admin.contrib.sqla import ModelView

from application.models import db, Event, Participant, Enrollment, Location


class ParticipantView(ModelView):
    column_exclude_list = ['password']

    form_widget_args = {
        'password': {
            'type': 'password'
        }
    }


def init_admin(admin):
    admin.add_view(ModelView(Event, db.session))
    admin.add_view(ParticipantView(Participant, db.session))
    admin.add_view(ModelView(Enrollment, db.session))
    admin.add_view(ModelView(Location, db.session))
