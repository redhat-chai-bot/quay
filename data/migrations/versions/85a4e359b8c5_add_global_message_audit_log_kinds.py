"""add global message audit log kinds

Revision ID: 85a4e359b8c5
Revises: b30800b1d271
Create Date: 2026-07-13 15:36:05.430608

"""

# revision identifiers, used by Alembic.
revision = "85a4e359b8c5"
down_revision = "b30800b1d271"

import sqlalchemy as sa


def upgrade(op, tables, tester):
    op.bulk_insert(
        tables.logentrykind,
        [
            {"name": "global_message_create"},
            {"name": "global_message_delete"},
        ],
    )


def downgrade(op, tables, tester):
    op.execute(
        tables.logentrykind.delete().where(
            tables.logentrykind.c.name.in_(
                [
                    "global_message_create",
                    "global_message_delete",
                ]
            )
        )
    )
