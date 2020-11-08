from django.urls import path
from .views import *

urlpatterns = [
    path('api-token-auth/', AppToken.as_view()),
    path('UserAPI/', UserAPI.as_view()),
    path('CreateUserRegister/', CreateUserRegister.as_view()),
    path('UserEditProfile/', UserEditProfile.as_view()),
    path('UserDeleteProfile/', UserDeleteProfile.as_view()),
]

