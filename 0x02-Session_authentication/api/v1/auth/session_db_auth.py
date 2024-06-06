#!/usr/bin/env python3
"""module for the class SessionDBAuth"""

from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from datetime import datetime, timedelta


class SessionDBAuth(SessionExpAuth):
    """essionDBAuth class extends SessionExpAuth with session management"""
    def create_session(self, user_id=None):
        """Creates a new session and saves it to a file-based storage."""
        session_id = super().create_session(user_id)
        if not session_id:
            return None
        args = {"user_id": user_id, "session_id": session_id}
        user_session = UserSession(**args)
        user_session.save()
        user_session.save_to_file()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Retrieves the user_id associated with the given session_id."""
        if not session_id:
            return None

        UserSession.load_from_file()
        user_session = UserSession.search({'session_id': session_id})
        if not user_session:
            return None

        user_session = user_session[0]

        ex = user_session.created_at + timedelta(seconds=self.session_duration)
        if ex < datetime.utcnow():
            return None

        return user_session.user_id

    def destroy_session(self, request=None):
        """Destroys the session associated with the given request."""
        if not request:
            return False
        session_id = self.session_cookie(request)
        if not session_id or not self.user_id_for_session_id(session_id):
            return False
        user_session = UserSession.search({"session_id": session_id})
        if not user_session:
            return False
        user_session[0].remove()
        UserSession.save_to_file()
        return True
