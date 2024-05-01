# controllers.py

from user_schema import User
import authentication

def authenticate_user(username, password):
    return authentication.authenticate_user(username, password)

def register_user(username, password):
    return authentication.register_user(username, password)
