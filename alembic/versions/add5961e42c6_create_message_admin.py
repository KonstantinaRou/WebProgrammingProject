"""create message admin

Revision ID: add5961e42c6
Revises: 
Create Date: 2016-05-13 16:55:06.676515

"""

# revision identifiers, used by Alembic.
revision = 'add5961e42c6'
down_revision = None
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa



def upgrade():
	op.create_table( #ananewnei thn vash me neo pinaka 
	    'message',
	    sa.Column('id', sa.Integer, primary_key=True),
	    sa.Column('user_to', sa.Integer, sa.ForeignKey("user.id"), nullable=False),
	    sa.Column('user_from', sa.Integer, sa.ForeignKey("user.id"), nullable=False),
	    sa.Column('message',sa.String(256),nullable=True)
    )

def downgrade():
	op.drop_table (
    	'message'
    )