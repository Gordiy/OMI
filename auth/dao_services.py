"""DAO services for auth app."""
import requests
from django.conf import settings

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
        user_data_url = 'https://api.linkedin.com/v2/userinfo'
        headers = {'Authorization': f'Bearer {access_token}'}
        user_response = requests.get(user_data_url, headers=headers)

        return user_response.json()
