"""Create a user account from the command line (e.g. your first account on a new database).

Usage (from apps/api): uv run python -m scripts.create_user alice@example.com
The password is asked interactively, so it never ends up in your shell history.
"""

import argparse
import getpass
import sys

from pydantic import ValidationError

from app.core.database import SessionLocal
from app.schemas.user import UserCreate
from app.services import users


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("email")
    email = parser.parse_args().email

    password = getpass.getpass("Password: ")
    if getpass.getpass("Repeat password: ") != password:
        print("Passwords do not match.", file=sys.stderr)
        return 1

    try:
        data = UserCreate(email=email, password=password)
    except ValidationError as error:
        print(error, file=sys.stderr)
        return 1

    with SessionLocal() as db:
        try:
            user = users.create_user(db, data)
        except users.EmailAlreadyRegisteredError:
            print(f"A user with the email {email} already exists.", file=sys.stderr)
            return 1

    print(f"Created user {user.email} ({user.id})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
