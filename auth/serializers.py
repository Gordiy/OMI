"""Serializers for auth app."""
from rest_framework import serializers

from .services import UserAuthorizationService


class LinkedInCallbackSerializer(serializers.Serializer):
    """The serializer used for LinkedIn authentication."""
    code = serializers.CharField()
    state = serializers.CharField()


class ValidateLinkedInAuthTokenSerializer(serializers.Serializer):
    """The serializer used to validate LinkedIn Auth."""
    jwt_token = serializers.CharField()

    def validate_jwt_token(self, token: str) -> str:
        UserAuthorizationService(authorization_code=None).validate_access_token(token)
        return token
