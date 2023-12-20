"""Views for auth app."""
import uuid

import requests
from django.conf import settings
from django.shortcuts import redirect
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .constants import LINKEDIN_OAUTH_URL
from .serializers import LinkedInCallbackSerializer


class LinkedInAuthorizationView(APIView):
    def get(self, request, *args, **kwargs):
        state = str(uuid.uuid4())
        authorization_url = f'{LINKEDIN_OAUTH_URL}authorization?response_type=code&client_id={settings.LINKEDIN_CLIENT_ID}&redirect_uri={settings.LINKEDIN_REDIRECT_URI}&state={state}&scope=profile%20email%20openid'
        return redirect(authorization_url)


class LinkedInCallbackView(APIView):
    def get(self, request, *args, **kwargs):
        serializer = LinkedInCallbackSerializer(data=request.GET, context={'request': request})
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        code = validated_data['code']

        # Check state for security
        # Perform token exchange to get access token
        access_token_url = f'{LINKEDIN_OAUTH_URL}accessToken'
        params = {
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': settings.LINKEDIN_REDIRECT_URI,
            'client_id': settings.LINKEDIN_CLIENT_ID,
            'client_secret': settings.LINKEDIN_CLIENT_SECRET,
        }
        response = requests.post(access_token_url, data=params)
        access_token = response.json().get('access_token')

        # Use the access token to fetch user data
        user_data_url = 'https://api.linkedin.com/v2/userinfo'
        headers = {'Authorization': f'Bearer {access_token}'}
        user_response = requests.get(user_data_url, headers=headers)
        user_data = user_response.json()

        # Extract relevant user data (adjust as needed)
        linkedin_id = user_data.get('id')
        first_name = user_data.get('localizedFirstName')
        last_name = user_data.get('localizedLastName')
        email = user_data.get('emailAddress')

        # Process or save the user data as needed
        # For simplicity, return user data as JSON
        return Response({
            'linkedin_id': linkedin_id,
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
        }, status=status.HTTP_200_OK)
