import json

import requests
from flask_apispec.views import MethodResource
from flask_apispec import use_kwargs
from flask import session
from flask_restful import Resource, request
from flask.json import jsonify
from marshmallow import Schema, fields
from requests.structures import CaseInsensitiveDict

import app
from core.models import User, db
from functools import wraps
from resources.imports import *
from resources.schemas import *


def check_for_session(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        user_id = session.get("user_id")
        if not user_id:
            return jsonify({"error": "Unauthorized"})
        return func(*args, **kwargs)

    return wrapped


class UserRequestSchema(Schema):
    Name = fields.String(required=True, description="Name")
    Email = fields.String(required=True, description="Email")
    Password = fields.String(required=True, description="Password")


class LoginRequestSchema(Schema):
    Name = fields.String(required=True, description="Name")
    Password = fields.String(required=True, description="Password")


class RegisterUser(MethodResource, Resource):
    @doc(description='Users', tags=['Users'])
    @use_kwargs(UserRequestSchema)
    def post(self, **kwargs):
        data = request.get_json(force=True)
        my_json = request.data.decode('utf8')
        decoded_data = json.loads(my_json)

        user_exists = User.query.filter_by(email=decoded_data["Email"]).first() is not None

        if user_exists:
            return jsonify({"error": "User already exist with this email"})

        hashed_password = app.bcrypt.generate_password_hash(decoded_data["Password"])
        # hashed_password = generate_password_hash(decoded_data["Password"])
        new_user = User(name=data["Name"], email=data["Email"], password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        session["user_id"] = new_user.id

        return jsonify({'Success': "Record added successfully."})


class Login(MethodResource, Resource):
    @doc(description='Users', tags=['Users'])
    @use_kwargs(LoginRequestSchema)
    def post(self, **kwargs):
        data = request.get_json(force=True)
        my_json = request.data.decode('utf8')
        decoded_data = json.loads(my_json)

        user = User.query.filter_by(name=decoded_data["Name"]).first()

        if user is None:
            return jsonify({"error": "Unauthorized"})


        if not app.bcrypt.check_password_hash(user.password, decoded_data["Password"]):
            return jsonify({"error": "Unauthorized"})

        session["user_id"] = user.id

        # get token
        headers = CaseInsensitiveDict()
        headers["Accept"] = "application/json"


        token = ""
        # Set environment variables
        os.environ['uname'] = decoded_data["Name"]
        os.environ['upass'] = decoded_data["Password"]

        headers["Username"] = os.environ['uname']
        headers["Password"] = os.environ['upass']
        url_get_login = "http://172.16.47.223:5000/contract/token/"
        resp1 = requests.get(url_get_login, headers=headers)
        token=resp1.json()['token']
        os.environ['token'] = token
        return jsonify(
            {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                'token':token
            }
        )


class Logout(MethodResource, Resource):
    @doc(description='Users', tags=['Users'])
    #@check_for_session
    def get(self):
        session.pop("user_id")
        return jsonify({"logout": "logout successfully"})


class DeleteUser(MethodResource, Resource):
    @doc(description='Users', tags=['Users'])
    #@check_for_session
    def get(self,email):
        user = User.query.filter_by(email=email).first()
        db.session.delete(user)
        db.session.commit()
        return jsonify({"Success": "Record has been deleted successfully"})


class AllUsers(MethodResource, Resource):
    @doc(description='Users', tags=['Users'])
    #@check_for_session
    def get(self, **kwargs):
        users_data=[]
        users = User.query.all()
        for user in users:
            data={
                'id':user.id,
                'email':user.email,
            }
            users_data.append(data)
        data_dump =json.dumps(users_data)
        response=json.loads(data_dump)
        return jsonify({'response':response})
