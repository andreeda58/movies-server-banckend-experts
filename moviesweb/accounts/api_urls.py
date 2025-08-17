from django.urls import path
from .api_views import CustomAuthToken, register_user, logout_user

urlpatterns = [
    path('login/',    CustomAuthToken.as_view(), name='login'),
    path('register/', register_user,             name='register'),
    path('logout/',   logout_user,               name='logout'),
]