"""Services for auth app."""
from rest_framework.exceptions import ValidationError

from .dao_services import UserAuthorizationDAOService
from .enums import UserAuthorizationErrorsEnum


class UserAuthorizationService:
    """Service to authorize user on LinkedIn."""
    def get_user(self, code: str) -> dict:
        """
        Get user data.

        :param code: authorization code.

        :raises ValidationError: access token not received.
        :raises ValidationError: user information not received.

        :return: user information such as name, surname and email.
        """
        access_token = UserAuthorizationDAOService.get_access_token(code)

        if not access_token:
            raise ValidationError(detail=UserAuthorizationErrorsEnum.TOKEN_NOT_RECEIVED.value)

        user_data = UserAuthorizationDAOService.get_user_data(access_token)

        error = user_data.get('error_description')
        if error:
            raise ValidationError(UserAuthorizationErrorsEnum.USER_INFO_NOT_RECEIVED.value.format(error=error))

        name = user_data.get('given_name')
        surname = user_data.get('given_name')
        email = user_data.get('email')

        return {
            'name': name,
            'surname': surname,
            'email': email
        }
