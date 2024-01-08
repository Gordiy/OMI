"""Services for auth app."""
from django.conf import settings
from django.shortcuts import redirect
from rest_framework.exceptions import AuthenticationFailed

from .dao_services import UserAuthorizationDAOService


class UserAuthorizationService:
    """
    Service for authorizing users on LinkedIn.
    """
    def __init__(self, authorization_code: str) -> None:
        """
        Initialize the service with the provided authorization code.

        :param authorization_code: The LinkedIn authorization code.
        """
        self._authorization_code = authorization_code
        self._dao_service = UserAuthorizationDAOService

    def save_user_data(self) -> str:
        """
        Save user data from LinkedIn.

        :raises ValidationError: Raised if access token is not received or user information is not received.

        :return: LinkedIn access_token.
        """
        access_token = self._dao_service.get_access_token(self._authorization_code)

        if not access_token:
            return redirect(settings.CANCEL_REDIRECT_URI)

        user_data = self._dao_service.get_user_data(access_token)

        error = user_data.get('error_description')
        if error:
            return redirect(settings.CANCEL_REDIRECT_URI)

        name = user_data.get('given_name')
        surname = user_data.get('family_name')
        email = user_data.get('email')

        self._dao_service.save_user(email, email, name, surname)
        return access_token

    def validate_access_token(self, access_token: str) -> bool:
        """
        Validate auth LinkedIn access token.
        
        :param access_token: access token received from LinkedIn.

        :return: True if user is authorized.
        """
        userinfo_response = self._dao_service.request_userinfo(access_token)

        if userinfo_response.status_code != 200:
            raise AuthenticationFailed()
        
        return True
