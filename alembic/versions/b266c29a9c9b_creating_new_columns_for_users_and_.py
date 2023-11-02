"""creating new columns for users and photos + detected photo table

Revision ID: b266c29a9c9b
Revises: b3fdd9433070
Create Date: 2023-07-05 19:36:49.656332

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b266c29a9c9b'
down_revision = 'b3fdd9433070'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('detected_photos',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('url', sa.String(), nullable=False),
    sa.Column('is_detection_correct', sa.Boolean(), nullable=True),
    sa.Column('is_favorite', sa.Boolean(), nullable=True),
    sa.Column('owner_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['owner_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name'),
    sa.UniqueConstraint('url')
    )
    op.create_index(op.f('ix_detected_photos_id'), 'detected_photos', ['id'], unique=False)
    op.add_column('photos', sa.Column('is_favorite', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('photos', 'is_favorite')
    op.drop_index(op.f('ix_detected_photos_id'), table_name='detected_photos')
    op.drop_table('detected_photos')
    # ### end Alembic commands ###