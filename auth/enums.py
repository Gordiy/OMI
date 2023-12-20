"""Enums for auth app."""
from enum import Enum


class UserAuthorizationErrorsEnum(Enum):
    """Errors raised by UserAuthorizationService."""
    TOKEN_NOT_RECEIVED = 'Access token not receive.'
    USER_INFO_NOT_RECEIVED = 'User information not received: {error}.'
