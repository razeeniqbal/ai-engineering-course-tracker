"""Server-side admin commands. There is no sign-up page; the owner account is made here.

    python -m app.cli create-owner --email you@example.com
    python -m app.cli reset-password --email you@example.com
    python -m app.cli unlock --email you@example.com
    python -m app.cli import-course course/AI_Engineering_Course_Razeen_v7.md --label v7
"""

import argparse
import getpass
import os
import sys
from pathlib import Path

from sqlalchemy import func, select

from app.db import SessionLocal
from app.importer import CourseImportError, import_course
from app.models import User
from app.security import check_new_password, hash_password


def _read_password() -> str:
    # OWNER_PASSWORD lets you script this in a one-off container; otherwise prompt.
    password = os.getenv("OWNER_PASSWORD") or getpass.getpass("Password: ")
    if not os.getenv("OWNER_PASSWORD") and password != getpass.getpass("Repeat password: "):
        sys.exit("Passwords don't match.")
    check_new_password(password)
    return password


def create_owner(email: str) -> None:
    with SessionLocal() as db:
        if db.scalar(select(func.count()).select_from(User)):
            sys.exit("An owner account already exists. Version 1 supports one user.")
        db.add(User(email=email.strip().lower(), password_hash=hash_password(_read_password())))
        db.commit()
    print(f"Created owner {email}")


def _get_user(db, email: str) -> User:
    user = db.scalar(select(User).where(User.email == email.strip().lower()))
    if user is None:
        sys.exit(f"No user with email {email}")
    return user


def reset_password(email: str) -> None:
    with SessionLocal() as db:
        user = _get_user(db, email)
        user.password_hash = hash_password(_read_password())
        user.session_version += 1
        user.failed_login_count, user.locked_until = 0, None
        db.commit()
    print("Password reset; all sessions signed out.")


def unlock(email: str) -> None:
    with SessionLocal() as db:
        user = _get_user(db, email)
        user.failed_login_count, user.locked_until = 0, None
        db.commit()
    print("Account unlocked.")


def import_course_file(path: str, label: str | None) -> None:
    markdown = Path(path).read_text(encoding="utf-8-sig")
    with SessionLocal() as db:
        try:
            version = import_course(db, markdown, label)
        except CourseImportError as exc:
            sys.exit("Import failed:\n- " + "\n- ".join(exc.errors))
        print(f"Imported course {version.label}")


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(prog="python -m app.cli")
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("create-owner", "reset-password", "unlock"):
        sub.add_parser(name).add_argument("--email", required=True)
    imp = sub.add_parser("import-course")
    imp.add_argument("path")
    imp.add_argument("--label")
    args = parser.parse_args(argv)
    try:
        if args.command == "create-owner":
            create_owner(args.email)
        elif args.command == "reset-password":
            reset_password(args.email)
        elif args.command == "unlock":
            unlock(args.email)
        else:
            import_course_file(args.path, args.label)
    except ValueError as exc:
        sys.exit(str(exc))


if __name__ == "__main__":
    main()
