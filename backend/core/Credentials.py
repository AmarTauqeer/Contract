import os
from flask import request, jsonify
from functools import wraps
import jwt


class Credentials():

    def get_username(self):
        username = os.getenv("user_name")
        return username

    def get_password(self):
        password = os.getenv("password")
        return password
    # check token

    def check_for_token(func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            # token = os.getenv("token")
            token = request.headers.get('Authorization')
            if token=='':
                return jsonify({'message': 'Token is missed'})
            try:
                # remove bearer keyword and a space
                bearer_free_token = token[7:]
                data = jwt.decode(bearer_free_token, os.getenv('SECRET_KEY'))
                print(data)
            except:
                return jsonify({'message': 'invalid token'})
            return func(*args, **kwargs)
        return wrapped
