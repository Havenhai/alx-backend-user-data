#!/usr/bin/env python3
"""module for the class Auth"""

from flask import request
from typing import List, TypeVar
from fnmatch import fnmatch
from os import getenv


class Auth:
    """A class handling authentication-related functionality."""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Determines if authentication is required for the given path."""
        if not path or not excluded_paths:
            return True
        if path[-1] != '/':
            path += '/'
        return not [n for n in excluded_paths if fnmatch(path, n)]

    def authorization_header(self, request=None) -> str:
        """Retrieves the authorization header from the provided request."""
        if not request:
            return None
        return request.headers.get('Authorization', None)

    def current_user(self, request=None) -> TypeVar("User"):
        """Retrieves the current user based on the provided request."""
        return None

    def session_cookie(self, request=None):
        """Retrieves a cookie value from a provided request."""
        if not request:
            return None
        return request.cookies.get(getenv('SESSION_NAME'), None)
