"""Serializers for auth app."""
from rest_framework import serializers


class LinkedInCallbackSerializer(serializers.Serializer):
    """The serializer used for LinkedIn authentication."""
    code = serializers.CharField()
    state = serializers.CharField()

