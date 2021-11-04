from flask import json, jsonify
from flask_restful import Resource, request
from flask_apispec.views import MethodResource
from flask_apispec import marshal_with, doc, use_kwargs
from marshmallow import Schema, fields
from functools import wraps
import jwt
import os
import re
from datetime import datetime, timedelta
from core.query_processor.QueryProcessor import QueryEngine
from core.contract_validation.ContractValidation import ContractValidation
from core.agent_validation.AgentValidation import AgentValidation
from tests.contract_test import ContractApiTest
import unittest
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
                        'exp': datetime.utcnow() + timedelta(days=100)
                    }, secret_key)
                    return jsonify({'token': token.decode('UTF-8')})
                else:
                    return 'username or password is not correct'
            elif request.headers.get('username') and request.headers.get('password'):
                if request.headers.get('username') == username and request.headers.get('password') == password:
                    token = jwt.encode({
                        'username': username,
                        'exp': datetime.utcnow() + timedelta(days=100)
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


class AgentRequestSchema(Schema):
    AgentId = fields.String(required=True, description="Agent ID")
    AgentType = fields.String(required=True, description="Agent Type")
    Name = fields.String(required=True, description="Name")
    Email = fields.String(required=False, description="Email")
    Phone = fields.String(required=False, description="Phone Number")
    Address = fields.String(required=True, description="Street Address")
    City = fields.String(required=False, description="City")
    State = fields.String(required=False, description="State")
    Country = fields.String(required=False, description="Country")


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
    # @marshal_with(BulkResponseQuerySchema)
    def get(self):
        query = QueryEngine()
        response = json.loads(
            query.select_query_gdb(purpose=None, dataRequester=None, additionalData="bcontractId", contractId=None,
                                   contractRequester=None, contractProvider=None))
        response = response["results"]
        return response, 200


class ContractByRequester(MethodResource, Resource):
    # @Credentials.check_for_token
    # @marshal_with(BulkResponseQuerySchema)
    def get(self, requester):
        query = QueryEngine()
        response = json.loads(
            query.select_query_gdb(purpose=None, dataRequester=None, additionalData="contractId", contractId=None,
                                   contractRequester=requester, contractProvider=None))
        response = response["results"]
        return response, 200


class ContractByProvider(MethodResource, Resource):
    # @Credentials.check_for_token
    # @marshal_with(BulkResponseQuerySchema)
    def get(self, provider):
        query = QueryEngine()
        response = json.loads(
            query.select_query_gdb(purpose=None, dataRequester=None, additionalData="contractId", contractId=None,
                                   contractRequester=None, contractProvider=provider))
        response = response["results"]
        return response, 200


class ContractByContractId(MethodResource, Resource):
    # @Credentials.check_for_token
    # @marshal_with(BulkResponseQuerySchema)
    def get(self, contractId):
        query = QueryEngine()
        response = json.loads(
            query.select_query_gdb(purpose=None, dataRequester=None, additionalData="contractId", contractId=contractId,
                                   contractRequester=None, contractProvider=None))
        res = jsonify(response["results"])
        res.status_code = 200
        return res


class ContractUpdate(MethodResource, Resource):
    # @Credentials.check_for_token
    @marshal_with(BulkResponseQuerySchema)
    @use_kwargs(ContractRequestSchema)
    def put(self, **kwargs):
        schema_serializer = ContractRequestSchema()
        data = request.get_json(force=True)
        contract_id = data['ContractId']
        # get contract status from db
        result = ContractByContractId.get(self, contract_id)
        my_json = result.data.decode('utf8')
        decoded_data = json.loads(my_json)
        status_value = decoded_data['bindings'][0]['ContractStatus']['value']
        signed = re.findall(r"Signed", status_value)
        if len(signed) == 0:
            validated_data = schema_serializer.load(data)
            cv = ContractValidation()
            response = cv.post_data(validated_data, type="update")
            if (response):
                return response
            else:
                return jsonify({'Error': "Record not updated due to some errors."})
        else:
            return jsonify({'Error': "Contract can't be modified after signed"})


class ContractCreate(MethodResource, Resource):
    # @Credentials.check_for_token
    @use_kwargs(ContractRequestSchema)
    def post(self, **kwargs):
        schema_serializer = ContractRequestSchema()
        data = request.get_json(force=True)
        contract_id = data['ContractId']
        # get contract status from db
        result = ContractByContractId.get(self, contract_id)
        my_json = result.data.decode('utf8')
        decoded_data = json.loads(my_json)

        if len(decoded_data['bindings']) == 1:
            return jsonify({'Error': "Contract id already exist"})
        else:
            validated_data = schema_serializer.load(data)
            cv = ContractValidation()
            response = cv.post_data(validated_data, type="insert")
            if (response):
                return jsonify({'Success': "Record inserted successfully."})
            else:
                return jsonify({'Error': "Record not inserted due to some errors."})


class AgentUpdate(MethodResource, Resource):
    # @Credentials.check_for_token
    @marshal_with(BulkResponseQuerySchema)
    @use_kwargs(AgentRequestSchema)
    def put(self, **kwargs):
        schema_serializer = AgentRequestSchema()
        data = request.get_json(force=True)
        agent_id = data['AgentId']
        # get contract status from db
        result = AgentByAgentId.get(self, agent_id)
        my_json = result.data.decode('utf8')
        decoded_data = json.loads(my_json)
        if len(decoded_data) > 0:
            validated_data = schema_serializer.load(data)
            av = AgentValidation()
            response = av.post_data(validated_data, type="update")
            if (response):
                return response
            else:
                return jsonify({'Error': "Record not updated due to some errors."})
        else:
            return jsonify({'Error': "Record doesn't exist ."})


class AgentByAgentId(MethodResource, Resource):
    # @Credentials.check_for_token
    # @marshal_with(BulkResponseQuerySchema)
    def get(self, agentId):
        query = QueryEngine()
        response = json.loads(
            query.select_query_gdb(purpose=None, dataRequester=None, additionalData="agentId", contractId=None,
                                   contractRequester=None, contractProvider=None, agentId=agentId))
        res = jsonify(response["results"])
        res.status_code = 200
        return res


class AgentCreate(MethodResource, Resource):
    # @Credentials.check_for_token
    @use_kwargs(AgentRequestSchema)
    def post(self, **kwargs):
        schema_serializer = AgentRequestSchema()
        data = request.get_json(force=True)
        agent_id = data['AgentId']
        # get agent from db
        result = AgentByAgentId.get(self, agent_id)
        my_json = result.data.decode('utf8')
        decoded_data = json.loads(my_json)

        if len(decoded_data['bindings']) == 1:
            return jsonify({'Error': "Agent id already exist"})
        else:
            validated_data = schema_serializer.load(data)
            av = AgentValidation()

            response = av.post_data(validated_data, type="insert")
            if (response):
                return jsonify({'Success': "Record inserted successfully."})
            else:
                return jsonify({'Error': "Record not inserted due to some errors."})


class AgentDeleteById(MethodResource, Resource):
    # @Credentials.check_for_token
    # @marshal_with(BulkResponseQuerySchema)
    # @use_kwargs(ContractRequestSchema)
    def delete(self, agentId):
        # get contract status from db
        result = AgentByAgentId.get(self, agentId)
        my_json = result.data.decode('utf8')
        decoded_data = json.loads(my_json)
        if len(decoded_data['bindings']) == 1:
            av = AgentValidation()
            response = av.delete_agent(agentId)
            if (response):
                return jsonify({'Success': "Record deleted successfully."})
            else:
                return jsonify({'Error': "Record not deleted due to some errors."})


class ContractDeleteById(MethodResource, Resource):
    # @Credentials.check_for_token
    # @marshal_with(BulkResponseQuerySchema)
    # @use_kwargs(ContractRequestSchema)
    def delete(self, contractId):
        # get contract status from db
        result = ContractByContractId.get(self, contractId)
        my_json = result.data.decode('utf8')
        decoded_data = json.loads(my_json)
        if len(decoded_data['bindings']) == 1:
            status_value = decoded_data['bindings'][0]['ContractStatus']['value']
            signed = re.findall(r"Signed", status_value)
            if len(signed) == 0:
                cv = ContractValidation()
                response = cv.delete_contract(contractId)
                if (response):
                    return jsonify({'Success': "Record deleted successfully."})
                else:
                    return jsonify({'Error': "Record not deleted due to some errors."})
            else:
                return jsonify({'Error': "Contract can't be deleted after signed"})
        else:
            return jsonify({'Error': "Contract doesn't exist"})


class GetAgents(MethodResource, Resource):
    # @Credentials.check_for_token
    # @marshal_with(BulkResponseQuerySchema)
    def get(self):
        query = QueryEngine()
        response = json.loads(
            query.select_query_gdb(purpose=None, dataRequester=None, additionalData="agents", contractId=None,
                                   contractRequester=None, contractProvider=None, ))
        response = response["results"]
        return response, 200

#
# class GetContractTestResult(MethodResource, Resource):
#     # @Credentials.check_for_token
#     # @marshal_with(BulkResponseQuerySchema)
#     def get(self):
#         response=ContractApiTest.test_get_all_contracts()
#         return response, 200
