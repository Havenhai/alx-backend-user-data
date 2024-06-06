#!/usr/bin/env python3
"""module for the class UserSession"""

from models.base import Base


class UserSession(Base):
    """Representation of a user's session."""

    def __init__(self, *args: list, **kwargs: dict):
        """Initialize a UserSession with user and session information."""
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get("user_id")
        self.session_id = kwargs.get("session_id")
