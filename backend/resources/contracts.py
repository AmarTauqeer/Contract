from flask import json, jsonify
from flask_restful import Resource, request
from flask_apispec.views import MethodResource
from flask_apispec import marshal_with, doc, use_kwargs
from marshmallow import Schema, fields
from functools import wraps
import jwt
import os
from datetime import datetime, timedelta
from core.query_processor.QueryProcessor import QueryEngine
from core.contract_validation.ContractValidation import ContractValidation
from core.Credentials import Credentials


class NestedSchema(Schema):
    Contract = fields.Dict(
        required=True, keys=fields.Str(),
        values=fields.Str()
    )


class ForNestedSchema(Schema):
    data = fields.List(fields.String())


class GenerateToken(MethodResource, Resource):
    # check username and password
    def check_for_username_password(func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            username = os.getenv('user_name')
            password = os.getenv('password')
            secret_key = os.getenv('SECRET_KEY')

            if request.authorization and request.authorization.username and request.authorization.password:
                if request.authorization.username == username and request.authorization.password == password:
                    token = jwt.encode({
                        'username': username,
                        'exp': datetime.utcnow() + timedelta(minutes=30)
                    }, secret_key)
                    return jsonify({'token': token.decode('UTF-8')})
                else:
                    return 'username or password is not correct'
            elif request.headers.get('username') and request.headers.get('password'):
                if request.headers.get('username') == username and request.headers.get('password') == password:
                    token = jwt.encode({
                        'username': username,
                        'exp': datetime.utcnow() + timedelta(minutes=30)
                    }, secret_key)
                    return jsonify({'token': token.decode('UTF-8')})
                else:
                    return 'username or password is not correct'
            else:
                return 'Basic authentication is required.'
        return wrapped

    @check_for_username_password
    def get(self):
        return True


class ContractRequestSchema(Schema):
    ContractId = fields.String(required=True, description="Contract ID")
    ContractType = fields.String(required=True,
                                 description="Contract Type")
    Purpose = fields.String(required=True, description="For What Purpose")
    ContractRequester = fields.String(required=True,
                                      description="Contract Requester")
    ContractProvider = fields.String(required=True,
                                     description="Contract Provider")
    DataController = fields.String(required=True,
                                   description="Data Controller")
    StartDate = fields.Date(required=False,
                            description="Start Date")
    ExecutionDate = fields.Date(required=False,
                                description="Execution Date")
    EffectiveDate = fields.Date(required=False,
                                description="Effective Date")
    ExpireDate = fields.Date(required=False,
                             description="Expire Date")
    Medium = fields.String(required=False, description="Medium")
    Waiver = fields.String(required=False, description="Waiver")
    Amendment = fields.String(required=False, description="Amendment")
    ConfidentialityObligation = fields.String(
        required=False, description="Confidentiality Obligation")
    DataProtection = fields.String(
        required=False, description="Data Protection")
    LimitationOnUse = fields.String(
        required=False, description="Limitation On Use")
    MethodOfNotice = fields.String(
        required=False, description="Method Of Notice")
    NoThirdPartyBeneficiaries = fields.String(
        required=False, description="No Third Party Beneficiaries")
    PermittedDisclosure = fields.String(
        required=False, description="Permitted Disclosure")
    ReceiptOfNotice = fields.String(
        required=False, description="Receipt Of Notice")
    Severability = fields.String(required=False, description="Severability")
    TerminationForInsolvency = fields.String(
        required=False, description="Termination For Insolvency")
    TerminationForMaterialBreach = fields.String(
        required=False, description="Termination For Material Breach")
    TerminationOnNotice = fields.String(
        required=False, description="Termination On Notice")
    ContractStatus = fields.String(
        required=False, description="Contract Status")


class BulkResponseQuerySchema(Schema):
    bindings = fields.List(fields.Nested(NestedSchema), required=True)


class Contracts(MethodResource, Resource):
    # @Credentials.check_for_token
    @marshal_with(BulkResponseQuerySchema)
    def get(self):
        query = QueryEngine()
        response = json.loads(query.select_query_gdb(purpose=None, dataRequester=None, additionalData="bcontractId",  contractId=None,
                                                     contractRequester=None, contractProvider=None,))
        response = response["results"]
        return response, 200


class ContractByRequester(MethodResource, Resource):
    # @Credentials.check_for_token
    @marshal_with(BulkResponseQuerySchema)
    def get(self, requester):
        query = QueryEngine()
        response = json.loads(query.select_query_gdb(purpose=None, dataRequester=None, additionalData="contractId", contractId=None,
                                                     contractRequester=requester, contractProvider=None))
        response = response["results"]
        return response, 200


class ContractByProvider(MethodResource, Resource):
    # @Credentials.check_for_token
    @marshal_with(BulkResponseQuerySchema)
    def get(self, provider):
        query = QueryEngine()
        response = json.loads(query.select_query_gdb(purpose=None, dataRequester=None, additionalData="contractId", contractId=None,
                                                     contractRequester=None, contractProvider=provider))
        response = response["results"]
        return response, 200


class ContractByContractId(MethodResource, Resource):
    # @Credentials.check_for_token
    @marshal_with(BulkResponseQuerySchema)
    def get(self, contractId):
        query = QueryEngine()
        response = json.loads(query.select_query_gdb(purpose=None, dataRequester=None, additionalData="contractId", contractId=contractId,
                                                     contractRequester=None, contractProvider=None))
        res = jsonify(response["results"])
        res.status_code = 200
        return res


class ContractCreate(MethodResource, Resource):
    # @Credentials.check_for_token
    @use_kwargs(ContractRequestSchema)
    def post(self, **kwargs):
        schema_serializer = ContractRequestSchema()
        data = request.get_json(force=True)
        validated_data = schema_serializer.load(data)
        cv = ContractValidation()
        response = cv.post_data(validated_data)
        if(response):
            return jsonify({'Success': "Record inserted successfully."})
        else:
            return jsonify({'Error': "Record not inserted due to some errors."})
