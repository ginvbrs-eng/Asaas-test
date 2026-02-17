"""${message}"""

revision = ${repr(up_revision)}
down_revision = ${repr(down_revision)}
branch_labels = ${repr(branch_labels)}
depends_on = ${repr(depends_on)}


def upgrade() -> None:
    """Apply schema changes."""
    # TODO: autogenerate migration body.
    pass


def downgrade() -> None:
    """Rollback schema changes."""
    # TODO: autogenerate rollback body.
    pass
