"""Services for auth app."""
from rest_framework.exceptions import ValidationError

from .dao_services import UserAuthorizationDAOService
from .enums import UserAuthorizationErrorsEnum


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

    def get_user_data(self) -> dict:
        """
        Get user data from LinkedIn.

        :raises ValidationError: Raised if access token is not received or user information is not received.

        :return: User information including id, name, surname, and email.
        """
        access_token = self._dao_service.get_access_token(self._authorization_code)

        if not access_token:
            raise ValidationError(detail=UserAuthorizationErrorsEnum.TOKEN_NOT_RECEIVED.value)

        user_data = self._dao_service.get_user_data(access_token)

        error = user_data.get('error_description')
        if error:
            raise ValidationError(UserAuthorizationErrorsEnum.USER_INFO_NOT_RECEIVED.value.format(error=error))

        name = user_data.get('given_name')
        surname = user_data.get('family_name')
        email = user_data.get('email')

        self._dao_service.save_user(email, email, name, surname)

        return {
            'name': name,
            'surname': surname,
            'email': email
        }
