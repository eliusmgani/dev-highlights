from django.urls import path
# from rest_framework.authtoken.views import obtain_auth_token
from account.api.views import (
    registration_views,
    account_properties_view,
    update_account_view,
    ObtainAuthTokenView,
    does_account_exist_view,
    ChangePasswordView
)

app_name = "account"

urlpatterns = [
    path('register', registration_views, name="Register"),
    # path('login', obtain_auth_token, name="Login"),
    path('login', ObtainAuthTokenView.as_view(), name="Login"),
    path('properties', account_properties_view, name="Properties"),
    path('properties/update', update_account_view, name="Update"),
    path('change_password', ChangePasswordView.as_view(), name="Change_Password"),
    path('check_if_account_exist', does_account_exist_view, name="check_if_account_exists")
]