from django.contrib.auth import authenticate
from business_logic.exceptions.exceptions import NotFound


def authenticate_user(cred):
    user = authenticate(username=cred['email'], password=cred['password'])
    if not user:
        raise NotFound(cred['email'])
    return user
