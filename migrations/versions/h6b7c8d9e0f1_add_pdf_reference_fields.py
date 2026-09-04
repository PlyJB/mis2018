"""add budget reference fields used by petty cash PDFs

Revision ID: h6b7c8d9e0f1
Revises: g5a6b7c8d9e0
"""

from alembic import op
import sqlalchemy as sa


revision = "h6b7c8d9e0f1"
down_revision = "g5a6b7c8d9e0"
branch_labels = None
depends_on = None


def upgrade():
    for table in ("petty_cash_claim_details", "cash_advance_return_details"):
        with op.batch_alter_table(table, schema=None) as batch_op:
            batch_op.add_column(sa.Column("reference_number", sa.String(length=255), nullable=True))
            batch_op.add_column(sa.Column("reference_date", sa.Date(), nullable=True))
            batch_op.add_column(sa.Column("product_code_id", sa.String(length=12), nullable=True))
            batch_op.add_column(sa.Column("cost_center_id", sa.String(length=12), nullable=True))
            batch_op.add_column(sa.Column("iocode_id", sa.String(length=16), nullable=True))
            batch_op.create_foreign_key(
                f"fk_{table}_product_code_id", "product_codes", ["product_code_id"], ["id"]
            )
            batch_op.create_foreign_key(
                f"fk_{table}_cost_center_id", "cost_centers", ["cost_center_id"], ["id"]
            )
            batch_op.create_foreign_key(
                f"fk_{table}_iocode_id", "iocodes", ["iocode_id"], ["id"]
            )


def downgrade():
    for table in ("cash_advance_return_details", "petty_cash_claim_details"):
        with op.batch_alter_table(table, schema=None) as batch_op:
            batch_op.drop_constraint(f"fk_{table}_iocode_id", type_="foreignkey")
            batch_op.drop_constraint(f"fk_{table}_cost_center_id", type_="foreignkey")
            batch_op.drop_constraint(f"fk_{table}_product_code_id", type_="foreignkey")
            for column in ("iocode_id", "cost_center_id", "product_code_id", "reference_date", "reference_number"):
                batch_op.drop_column(column)
