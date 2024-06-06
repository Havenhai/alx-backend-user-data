#!/usr/bin/env python3
"""
Main file
"""
from auth import Auth
import requests

EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"
BASE_URL = "http://127.0.0.1:5000"


def register_user(email: str, password: str) -> None:
    """Registers a new user with the specified email and password."""
    pass


def log_in_wrong_password(email: str, password: str) -> None:
    """Attempts to log in with the specified email and incorrect password."""
    pass


def profile_unlogged() -> None:
    """Accesses the profile endpoint without logging in, expecting a 403."""
    pass


def log_in(email: str, password: str) -> str:
    """Logs in with the specified email and password, returning session ID"""
    return None


def profile_logged(session_id: str) -> None:
    """Accesses the profile endpoint with a valid session ID."""
    pass


def log_out(session_id: str) -> None:
    """Logs out the user with the specified session ID."""
    pass


def reset_password_token(email: str) -> str:
    """Requests a password reset token for the specified email."""
    return None


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """
    Updates the password for the specified email using the provided
    reset token and new password.
    """
    pass


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
