"""Views for auth app."""
import uuid

from django.conf import settings
from django.shortcuts import redirect
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .constants import LINKEDIN_OAUTH_URL
from .serializers import LinkedInCallbackSerializer
from .services import UserAuthorizationService


class LinkedInAuthorizationView(APIView):
    """
    View for initiating the LinkedIn OAuth 2.0 authorization process.

    This view generates a unique random string as the 'state' parameter,
    includes it in the LinkedIn authorization URL, and redirects the user
    to LinkedIn for authentication and authorization.
    """

    def get(self, request: Request, *args, **kwargs) -> Response:
        """
        Handles GET requests for initiating LinkedIn OAuth 2.0 authorization.

        :param request: The HTTP request.
        :param args: Additional positional arguments.
        :param kwargs: Additional keyword arguments.

        :return: Redirects the user to the LinkedIn authorization URL.
        """
        state = str(uuid.uuid4())
        authorization_url = f'{LINKEDIN_OAUTH_URL}authorization?response_type=code&client_id={settings.LINKEDIN_CLIENT_ID}&redirect_uri={settings.LINKEDIN_REDIRECT_URI}&state={state}&scope=profile%20email%20openid'
        return redirect(authorization_url)


class LinkedInCallbackView(APIView):
    """
    View for handling the callback after a successful LinkedIn OAuth 2.0 authorization.

    This view validates the callback parameters, exchanges the authorization code for an access token,
    and fetches user data from LinkedIn. The user data is then returned in the response.
    """
    def get(self, request: Request, *args, **kwargs) -> Response:
        """
        Handles GET requests for processing the LinkedIn OAuth 2.0 callback.

        :param request: The HTTP request.
        :param args: Additional positional arguments.
        :param kwargs: Additional keyword arguments.

        :return: JSON response containing LinkedIn user data.
        """
        serializer = LinkedInCallbackSerializer(data=request.GET)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        authorization_service = UserAuthorizationService(validated_data['code'])
        authorization_service.save_user_data()

        return redirect(settings.SUCCESS_REDIRECT_URI)
