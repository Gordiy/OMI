"""DAO services for auth app."""
import requests
from django.conf import settings
from django.contrib.auth.models import User

from .constants import LINKEDIN_OAUTH_URL


class UserAuthorizationDAOService:
    """DAO Service to authorize user on LinkedIn."""
    @staticmethod
    def get_access_token(code: str) -> str or None:
        """
        Get access token.
        
        :param code: authorization code.

        :return: access token.
        """
        access_token_url = f'{LINKEDIN_OAUTH_URL}accessToken'
        params = {
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': settings.LINKEDIN_REDIRECT_URI,
            'client_id': settings.LINKEDIN_CLIENT_ID,
            'client_secret': settings.LINKEDIN_CLIENT_SECRET,
        }
        response = requests.post(access_token_url, data=params)
        return response.json().get('access_token')
    
    @staticmethod
    def get_user_data(access_token: str) -> dict:
        """
        Get user data from LinkedIN.

        :param access_token: authorization access_token.

        :return: response data.
        """
        user_info = UserAuthorizationDAOService.request_userinfo(access_token)

        return user_info.json()
    
    @staticmethod
    def request_userinfo(access_token: str) -> requests.Response:
        """
        Request userinfo from LinkedIN.

        :param access_token: authorization access_token.

        :return: response.
        """
        user_data_url = 'https://api.linkedin.com/v2/userinfo'
        headers = {'Authorization': f'Bearer {access_token}'}
        return requests.get(user_data_url, headers=headers)
    
    @staticmethod
    def save_user(username: str, email: str, first_name: str, last_name: str) -> None:
        """
        Save or update a user in the Django User model based on the provided information.

        If a user with the specified `username` does not exist, a new user is created.
        If the user already exists, their information is updated with the provided data.

        :param username: The unique identifier for the user (e.g., email).
        :param email: The email address of the user.
        :param first_name: The first name of the user.
        :param last_name: The last name of the user.

        :return: None
        """
        user, created = User.objects.get_or_create(username=username, defaults={'email': email})
        
        if not created:
            user.username = username

        # Update user information
        user.first_name = first_name
        user.last_name = last_name
        user.email = email

        user.save()
