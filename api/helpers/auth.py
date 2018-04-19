"""
Helper functions to deal with authentication and authorization.
"""
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
    """
    Decrypt data.
    """
    cryptographic_key = getenv('CRYPTOGRAPHIC_KEY').encode('utf-8')
    f = Fernet(cryptographic_key)
    return eval((f.decrypt((data).encode('utf-8'))).decode('utf-8'))


def encrypt(data):
    """
    Encrypt data.
    """
    cryptographic_key = getenv('CRYPTOGRAPHIC_KEY').encode('utf-8')
    f = Fernet(cryptographic_key)
    return (f.encrypt(str(data).encode('utf-8'))).decode('utf-8')


def create_token(email):
    """
    Create access token and return it.
    """
    token_fields = ['id', 'email', 'name']
    user = User.get(email=email)
    user_roles = [role.title for role in user.roles]
    user = user.serialize()
    data = {field: user[field] for field in token_fields}
    data.update({'roles': user_roles})
    created = time()
    expires = created + timedelta(days=1000).total_seconds()
    data.update({'created': created, 'expires': expires})
    data = {'data': encrypt(data)}
    return encode(data, getenv('JWT_KEY'), algorithm='HS256').decode('utf-8')


def view_token(token):
    """
    View information inside token.
    """
    decoded = decode(
        token,
        getenv('JWT_KEY'),
        algorithms=['HS256'])
    decrypted = decrypt(decoded['data'])
    return decrypted


def token_required(f):
    """
    Protect view functions.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        """
        Wrap function.
        """
        token = request.headers.get('Authorization')
        if not token:
            return {
                "status": "fail",
                "error": "Bad request",
                "message": "Header does not contain authorization token."
            }, 400
        try:
            decode(
                token,
                getenv('JWT_KEY'),
                algorithms=['HS256'],
                options={
                    'verify_signature': True,
                    'verify_exp': True
                }
            )
            return f(*args, **kwargs)
        except Exception as e:
            return {
                "status": "fail",
                "error": "Bad request",
                "message": "There's a problem with the token.",
                "exception": e
            }, 400
    return decorated
