"""Fake objects that replace real dependencies in tests."""

from sqlalchemy.exc import OperationalError


class FakeSession:
    """Stands in for a SQLAlchemy session.

    Set `fail = True` to simulate a database that cannot be reached.
    """

    def __init__(self) -> None:
        self.fail = False

    def execute(self, statement: object) -> None:
        if self.fail:
            raise OperationalError(str(statement), {}, Exception("connection refused"))
