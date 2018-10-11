"""Helper functions to deal with authentication and authorization."""
from datetime import timedelta
from functools import wraps
from os import getenv
from time import time

from cryptography.fernet import Fernet
from flask import request
from jwt import decode, encode

from api.models import User

# pylint:disable=invalid-name, eval-used, broad-except


def decrypt(data):
    """Decrypt data."""
    cryptographic_key = getenv('CRYPTOGRAPHIC_KEY').encode('utf-8')
    f = Fernet(cryptographic_key)
    return eval((f.decrypt((data).encode('utf-8'))).decode('utf-8'))


def encrypt(data):
    """Encrypt data."""
    cryptographic_key = getenv('CRYPTOGRAPHIC_KEY').encode('utf-8')
    f = Fernet(cryptographic_key)
    return (f.encrypt(str(data).encode('utf-8'))).decode('utf-8')


def create_token(email):
    """Create access token and return it."""
    token_fields = ['id', 'email', 'name']
    user = User.get(email=email)
    user_roles = [role.title for role in user.roles]
    user = user.serialize()
    data = {field: user[field] for field in token_fields}
    data.update({'roles': user_roles})
    created = time()
    expires = created + timedelta(days=7).total_seconds()
    data = {'data': encrypt(data)}
    data.update({'expires': expires})
    return encode(data, getenv('JWT_KEY'), algorithm='HS256').decode('utf-8')


def view_token(token):
    """View information inside token."""
    decoded = decode(
        token,
        getenv('JWT_KEY'),
        algorithms=['HS256'])
    decrypted = decrypt(decoded['data'])
    return decrypted


def token_required(f):
    """Protect view functions."""
    @wraps(f)
    def decorated(*args, **kwargs):
        """Wrap function."""
        token = request.headers.get('Authorization')
        if not token:
            return {
                "status": "fail",
                "error": "Bad request",
                "message": "Header does not contain authorization token."
            }, 400
        try:
            decoded_token = decode(
                token,
                getenv('JWT_KEY'),
                algorithms=['HS256'],
                options={
                    'verify_signature': True
                }
            )
            if decoded_token['expires'] < time():
                return {
                    "status": "fail",
                    "error": "Bad request",
                    "message": "Expired token."
                }, 400
            else:
                return f(*args, **kwargs)
        except Exception as e:
            return {
                "status": "fail",
                "error": "Bad request",
                "message": str(e)
            }, 400
    return decorated


def requires_role(role):
    """Define the decorator's wrapper."""
    def check_role(f):
        """Confirm the user who made a request has a required role."""
        @wraps(f)
        def wrapper(request, *args, **kwargs):
            """Carry out check_role functionality."""
            token = request.headers.get('Authorization')
            decoded_token = decode(
                token,
                getenv('JWT_KEY'),
                algorithms=['HS256'],
                options={
                    'verify_signature': True})
            if role in decoded_token['roles']:
                return f(*args, **kwargs)
            else:
                return {
                    "status": "fail",
                    "error": "Bad request",
                    "message": "Unauthorized."
                }, 401
        return wrapper
    return check_role
