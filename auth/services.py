"""Services for auth app."""
from .dao_services import UserAuthorizationDAOService
from django.shortcuts import redirect
from django.conf import settings


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

    def save_user_data(self) -> None:
        """
        Save user data from LinkedIn.

        :raises ValidationError: Raised if access token is not received or user information is not received.

        :return:
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
