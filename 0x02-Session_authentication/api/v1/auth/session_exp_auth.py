#!/usr/bin/env python3
"""module for the class SessionExpAuth"""

from api.v1.auth.session_auth import SessionAuth
from os import getenv
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """Extension of SessionAuth with session expiration functionality."""

    def __init__(self):
        """Initialize SessionExpAuth with session duration configuration."""
        try:
            self.session_duration = int(getenv('SESSION_DURATION', 0))
        except ValueError:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """Create a new session with extended session details."""
        session_id = super().create_session(user_id)
        if not session_id:
            return None
        self.user_id_by_session_id[session_id] = {'user_id': user_id,
                                                  'created_at': datetime.now()}
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Retrieve the user_id linked to a session, considering expiration."""
        if not session_id:
            return None
        session_dict = super().user_id_for_session_id(session_id)
        if not session_dict:
            return None
        if self.session_duration <= 0:
            return session_dict.get('user_id', None)
        created_at = session_dict.get('created_at', None)
        if not created_at:
            return None
        exp = created_at + timedelta(seconds=self.session_duration)
        if exp < datetime.now():
            return None
        return session_dict.get('user_id', None)
