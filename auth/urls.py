# urls.py
from django.urls import path

from .views import (LinkedInAuthorizationView, LinkedInCallbackView,
                    ValidateLinkedInAuthTokenView)

urlpatterns = [
    path('linkedin-login/', LinkedInAuthorizationView.as_view(), name='linkedin-authorize'),
    path('linkedin-callback/', LinkedInCallbackView.as_view(), name='linkedin-callback'),
    path('validate-token/', ValidateLinkedInAuthTokenView.as_view(), name='linkedin-validate-token')
]
