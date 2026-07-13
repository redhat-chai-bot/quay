"""add global message audit log kinds

Revision ID: 5f952a301f5d
Revises: b30800b1d271
Create Date: 2026-07-13 15:30:00.000000

"""

# revision identifiers, used by Alembic.
revision = "5f952a301f5d"
down_revision = "b30800b1d271"


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
