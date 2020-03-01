from alembic import op
import sqlalchemy as sa
from sqlalchemy_utils import ChoiceType

from application.models import EventType, CategoryType

revision = '2c64850bb666'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('locations',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=80), nullable=False),
    sa.Column('code', sa.String(length=8), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('code'),
    sa.UniqueConstraint('title')
    )
    op.create_table('participants',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=False),
    sa.Column('email', sa.String(length=80), nullable=False),
    sa.Column('password', sa.String(length=80), nullable=False),
    sa.Column('picture', sa.String(length=80), nullable=True),
    sa.Column('location', sa.String(length=80), nullable=False),
    sa.Column('about', sa.String(length=180), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('events',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=80), nullable=False),
    sa.Column('description', sa.String(length=80), nullable=False),
    sa.Column('date', sa.Date(), nullable=False),
    sa.Column('time', sa.Time(), nullable=False),
    sa.Column('type', ChoiceType(EventType), nullable=False),
    sa.Column('category', ChoiceType(CategoryType), nullable=False),
    sa.Column('location_id', sa.Integer(), nullable=True),
    sa.Column('address', sa.String(length=80), nullable=False),
    sa.Column('seats', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['location_id'], ['locations.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('enrollments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('event_id', sa.Integer(), nullable=True),
    sa.Column('participant_id', sa.Integer(), nullable=True),
    sa.Column('datetime', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['event_id'], ['events.id'], ),
    sa.ForeignKeyConstraint(['participant_id'], ['participants.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('event_id', 'participant_id', name='event-participant-constraint')
    )


def downgrade():
    op.drop_table('enrollments')
    op.drop_table('events')
    op.drop_table('participants')
    op.drop_table('locations')
