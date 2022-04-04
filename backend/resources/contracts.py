import textwrap

import smtplib
import uuid

from core.storage.Sparql import SPARQL
from SPARQLWrapper import JSON, SPARQLWrapper, BASIC
from flask import json, jsonify
from flask_restful import Resource, request
from flask_apispec.views import MethodResource
from flask_apispec import marshal_with, doc, use_kwargs
from marshmallow import Schema, fields
from functools import wraps
import jwt
import os
import re
from datetime import *
from datetime import datetime, timedelta
from core.query_processor.QueryProcessor import QueryEngine
from core.contract_validation.ContractValidation import ContractValidation
from core.contractor_validation.ContractorValidation import ContractorValidation
from core.term_validation.term_validation import TermValidation
from core.obligation_validation.obligation_validation import ObligationValidation
from core.term_type_validation.term_type_validation import TermTypeValidation
from tests.contract_test import ContractApiTest
import unittest
from core.Credentials import Credentials

from resources.users import check_for_session


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


class ObligationRequestSchema(Schema):
    Description = fields.String(required=True, description="Description")
    TermId = fields.String(required=True, description="Term ID")
    ContractorId = fields.String(required=True, description="Contractor ID")
    ContractId = fields.String(required=True, description="Contract ID")
    State = fields.String(required=False, description="Obligation State")
    ExecutionDate = fields.Date(required=False, description="Execution Date")
    EndDate = fields.Date(required=False, description="End Date")


class ObligationUpdateSchema(Schema):
    ObligationId = fields.String(required=True, description="Obligation ID")
    Description = fields.String(required=True, description="Description")
    TermId = fields.String(required=True, description="Term ID")
    ContractorId = fields.String(required=True, description="Contractor ID")
    ContractId = fields.String(required=True, description="Contract ID")
    State = fields.String(required=False, description="Obligation State")
    ExecutionDate = fields.Date(required=False, description="Execution Date")
    EndDate = fields.Date(required=False, description="End Date")


class ContractorRequestSchema(Schema):
    Name = fields.String(required=True, description="Name")
    Email = fields.String(required=False, description="Email")
    Phone = fields.String(required=False, description="Phone Number")
    Address = fields.String(required=True, description="Street Address")
    Territory = fields.String(required=False, description="Territory")
    Country = fields.String(required=False, description="Country")
    Role = fields.String(required=False, description="Role")


class ContractorUpdateSchema(Schema):
    ContractorId = fields.String(required=True, description="Contractor ID")
    Name = fields.String(required=True, description="Name")
    Email = fields.String(required=False, description="Email")
    Phone = fields.String(required=False, description="Phone Number")
    Address = fields.String(required=True, description="Street Address")
    Territory = fields.String(required=False, description="Territory")
    Country = fields.String(required=False, description="Country")
    Role = fields.String(required=False, description="Role")


class TermTypeUpdateSchema(Schema):
    TermTypeId = fields.String(required=True, description="TermId")
    Name = fields.String(required=False, description="Name")
    Description = fields.String(required=False, description="Description")


class TermTypeRequestSchema(Schema):
    Name = fields.String(required=False, description="Name")
    Description = fields.String(required=False, description="Description")


class TermUpdateSchema(Schema):
    TermId = fields.String(required=True, description="TermId")
    TermTypeId = fields.String(required=True, description="TermTypeId")
    ContractId = fields.String(required=True, description="Contract ID")
    Description = fields.String(required=False, description="Description")


class TermRequestSchema(Schema):
    TermTypeId = fields.String(required=True, description="TermTypeId")
    ContractId = fields.String(required=True, description="Contract ID")
    Description = fields.String(required=False, description="Description")


class ContractUpdateSchema(Schema):
    ContractId = fields.String(required=True, description="Contract ID")
    ContractType = fields.String(required=True,
                                 description="Contract Type")
    Purpose = fields.String(required=True, description="For What Purpose")

    ExecutionDate = fields.Date(required=False,
                                description="Execution Date")
    EffectiveDate = fields.Date(required=False,
                                description="Effective Date")
    EndDate = fields.Date(required=False,
                          description="Expire Date")
    Medium = fields.String(required=False, description="Medium")

    ContractStatus = fields.String(
        required=False, description="Contract Status")

    ConsiderationDescription = fields.String(
        required=False, description="Consideration description")
    ConsiderationValue = fields.String(
        required=False, description="Consideration Value")
    ContractCategory = fields.String(
        required=False, description="Contract Category")
    Contractors = fields.List(fields.String(),
                              required=False, description="Contractors")
    Terms = fields.List(fields.String(),
                        required=False, description="Contract Terms")
    Obligations = fields.List(fields.String(),
                              required=False, description="Contract Obligations")


class ContractRequestSchema(Schema):
    ContractType = fields.String(required=True,
                                 description="Contract Type")
    Purpose = fields.String(required=True, description="For What Purpose")

    ExecutionDate = fields.Date(required=False,
                                description="Execution Date")
    EffectiveDate = fields.Date(required=False,
                                description="Effective Date")
    EndDate = fields.Date(required=False,
                          description="Expire Date")
    Medium = fields.String(required=False, description="Medium")

    ContractStatus = fields.String(
        required=False, description="Contract Status")

    ContractCategory = fields.String(
        required=False, description="Contract Category")

    ConsiderationDescription = fields.String(
        required=False, description="Consideration description")
    ConsiderationValue = fields.String(
        required=False, description="Consideration Value")
    Contractors = fields.List(fields.String(),
                              required=False, description="Contractors")
    Terms = fields.List(fields.String(),
                        required=False, description="Contract Terms")
    Obligations = fields.List(fields.String(),
                              required=False, description="Contract Obligations")


class BulkResponseQuerySchema(Schema):
    bindings = fields.List(fields.Nested(NestedSchema), required=True)


class Contracts(MethodResource, Resource):
    @doc(description='Contracts', tags=['Contracts'])
    # @check_for_session
    # @Credentials.check_for_token
    # @marshal_with(BulkResponseQuerySchema)
    def get(self):
        query = QueryEngine()
        response = json.loads(
            query.select_query_gdb(purpose=None, dataRequester=None, additionalData="bcontractId", contractID=None,
                                   contractRequester=None, contractProvider=None))

        if len(response["results"]['bindings']) != 0:
            data = response["results"]['bindings']
            all_data = []
            for d in data:
                contractor_array = []
                term_array = []
                obligation_array = []

                contid = d['Contract']['value']
                contid = contid[45:]
                # print(contid)

                # get contractors
                contractors = GetContractContractors.get(self, contid)
                contractors = contractors.json
                if contractors != 'No record found for this ID':
                    for c in contractors:
                        cid = c['contractorID']
                        contractor_array.append(cid)

                # get terms
                terms = GetContractTerms.get(self, contid)
                terms = terms.json
                if terms != 'No record found for this ID':
                    for t in terms:
                        tid = t['termID']
                        term_array.append(tid)

                # get obligation
                obl = GetObligationByContractId.get(self, contid)
                obl = obl.json
                if obl != 'No record found for this ID':
                    for o in obl:
                        oid = o['obligationID']
                        obligation_array.append(oid)

                obj = {
                    'contractors': contractor_array,
                    'terms': term_array,
                    'obligations': obligation_array
                }
                new_data = {
                    'Contract': d['Contract']['value'][45:],
                    'ContractStatus': d['ContractStatus']['value'][45:],
                    'ContractCategory': d['ContractCategory']['value'][45:],
                    'Purpose': d['Purpose']['value'],
                    'ContractType': d['ContractType']['value'][45:],
                    'EffectiveDate': d['EffectiveDate']['value'][45:],
                    'ExecutionDate': d['ExecutionDate']['value'][45:],
                    'EndDate': d['EndDate']['value'][45:],
                    'Medium': d['Medium']['value'],
                    'consideration': d['consideration']['value'],
                    'value': d['value']['value'],
                    'identifiers': obj
                }

                all_data.append(new_data)
            if len(all_data) != 0:
                return all_data
        return 'No record is found'


class ContractByContractor(MethodResource, Resource):
    @doc(description='Contracts', tags=['Contracts'])
    # @check_for_session
    # @Credentials.check_for_token
    # @marshal_with(BulkResponseQuerySchema)
    def get(self, contractorID):
        query = QueryEngine()
        response = json.loads(
            query.select_query_gdb(purpose=None, dataRequester=None, additionalData="contractByContractorID",
                                   contractorID=contractorID,
                                   contractRequester=None, contractProvider=None))
        response = response["results"]['bindings']
        if len(response) != 0:
            main_data = []
            for r in response:
                contract_id = r['Contract']['value'][45:]
                res = ContractByContractId.get(self, contract_id)
                # print(res.json)
                if res != 'No record found for this ID':
                    data = res.json
                    main_data.append(data)
            return main_data
        return 'No record found for this ID'


class ContractByProvider(MethodResource, Resource):
    # @check_for_session
    # @Credentials.check_for_token
    # @marshal_with(BulkResponseQuerySchema)
    def get(self, provider):
        query = QueryEngine()
        response = json.loads(
            query.select_query_gdb(purpose=None, dataRequester=None, additionalData="contractID", contractID=None,
                                   contractRequester=None, contractProvider=provider))
        response = response["results"]
        return response, 200


class ContractByContractId(MethodResource, Resource):
    @doc(description='Contracts', tags=['Contracts'])
    # @check_for_session
    # @Credentials.check_for_token
    # @marshal_with(BulkResponseQuerySchema)
    def get(self, contractID):

        query = QueryEngine()
        response = json.loads(
            query.select_query_gdb(purpose=None, dataRequester=None, additionalData="contractID", contractID=contractID,
                                   contractRequester=None, contractProvider=None, contractorID=None))

        data = response["results"]['bindings']
        if len(data) != 0:
            contractor_array = []
            term_array = []
            obligation_array = []

            for d in data:

                # get contractors
                contractors = GetContractContractors.get(self, contractID)
                contractors = contractors.json
                if contractors != 'No record found for this ID':
                    for c in contractors:
                        cid = c['contractorID']
                        contractor_array.append(cid)

                # get terms
                terms = GetContractTerms.get(self, contractID)
                terms = terms.json
                if terms != 'No record found for this ID':
                    for t in terms:
                        tid = t['termID']
                        term_array.append(tid)

                # get obligation
                obl = GetObligationByContractId.get(self, contractID)
                obl = obl.json

                if obl != 'No record found for this ID':
                    for o in obl:
                        oid = o['obligationID']
                        obligation_array.append(oid)

            obj = {
                'contractors': contractor_array,
                'terms': term_array,
                'obligations': obligation_array
            }
            new_data = {
                'Contract': d['Contract']['value'][45:],
                'ContractStatus': d['ContractStatus']['value'][45:],
                'ContractCategory': d['ContractCategory']['value'][45:],
                'Purpose': d['Purpose']['value'],
                'ContractType': d['ContractType']['value'][45:],
                'EffectiveDate': d['EffectiveDate']['value'][45:],
                'ExecutionDate': d['ExecutionDate']['value'][45:],
                'EndDate': d['EndDate']['value'][45:],
                'Medium': d['Medium']['value'],
                'consideration': d['consideration']['value'],
                'value': d['value']['value'],
                'identifiers': obj
            }
            data = new_data
            if len(data) != 0:
                return data
        return 'No data found for this ID'


class ContractUpdate(MethodResource, Resource):
    @doc(description='Contracts', tags=['Contracts'])
    # @check_for_session
    # @Credentials.check_for_token
    @marshal_with(BulkResponseQuerySchema)
    @use_kwargs(ContractUpdateSchema)
    def put(self, **kwargs):
        schema_serializer = ContractUpdateSchema()
        data = request.get_json(force=True)
        contract_id = data['ContractId']
        # get contract status from db
        result = ContractByContractId.get(self, contract_id)
        my_json = result.data.decode('utf8')
        decoded_data = json.loads(my_json)
        # print(decoded_data)
        if decoded_data != 'No data found for this ID':
            if decoded_data['Contract'] == contract_id:
                status_value = decoded_data['ContractStatus']
                signed = re.findall(r"Signed", status_value)
                if len(signed) == 0:
                    validated_data = schema_serializer.load(data)
                    cv = ContractValidation()
                    response = cv.post_data(validated_data, type="update", contract_id=None)
                    if (response):
                        return jsonify({'Success': "Record updated successfully"})
                    else:
                        return jsonify({'Error': "Record not updated due to some errors."})
                else:
                    return jsonify({'Error': "Contract can't be modified after signed"})
            return jsonify({'Error': "Contract doesn't match with this ID"})
        return jsonify({'Success': "No record found for this ID"})


class ContractCreate(MethodResource, Resource):
    @doc(description='Contracts', tags=['Contracts'])
    # @check_for_session
    # @Credentials.check_for_token
    @use_kwargs(ContractRequestSchema)
    def post(self, **kwargs):
        schema_serializer = ContractRequestSchema()
        data = request.get_json(force=True)
        uuidOne = uuid.uuid1()
        contract_id = "CONT_" + str(uuidOne)
        validated_data = schema_serializer.load(data)
        cv = ContractValidation()
        response = cv.post_data(validated_data, type="insert", contract_id=contract_id)
        if (response):
            return jsonify({'Success': "Record inserted successfully."})
        else:
            return jsonify({'Error': "Record not inserted due to some errors."})


class ContractorUpdate(MethodResource, Resource):
    @doc(description='Contractors', tags=['Contractors'])
    # @check_for_session
    # @Credentials.check_for_token
    @marshal_with(BulkResponseQuerySchema)
    @use_kwargs(ContractorUpdateSchema)
    def put(self, **kwargs):
        schema_serializer = ContractorUpdateSchema()
        data = request.get_json(force=True)
        contractor_id = data['ContractorId']
        # get contract status from db
        result = ContractorById.get(self, contractor_id)
        my_json = result.data.decode('utf8')
        decoded_data = json.loads(my_json)
        if len(decoded_data) > 0:
            validated_data = schema_serializer.load(data)
            av = ContractorValidation()
            response = av.post_data(validated_data, type="update", contractor_id=None)
            if (response):
                return response
            else:
                return jsonify({'Error': "Record not updated due to some errors."})
        else:
            return jsonify({'Error': "Record doesn't exist ."})


class ContractorById(MethodResource, Resource):
    @doc(description='Contractors', tags=['Contractors'])
    # @check_for_session
    # @Credentials.check_for_token
    # @marshal_with(BulkResponseQuerySchema)
    def get(self, contractorID):
        query = QueryEngine()
        response = json.loads(
            query.select_query_gdb(purpose=None, dataRequester=None, additionalData="contractorID", contractID=None,
                                   contractRequester=None, contractProvider=None, contractorID=contractorID))
        res = response["results"]['bindings']
        if len(res) > 0:
            data = {
                'ContractorID': res[0]['Contractor']['value'][45:],
                'name': res[0]['name']['value'],
                'phone': res[0]['phone']['value'],
                'email': res[0]['email']['value'],
                'country': res[0]['country']['value'],
                'territory': res[0]['territory']['value'],
                'address': res[0]['address']['value'],
            }
            return data
        return "No record is found for this ID"


class ContractorCreate(MethodResource, Resource):
    @doc(description='Contractors', tags=['Contractors'])
    # @check_for_session
    # @Credentials.check_for_token
    @use_kwargs(ContractorRequestSchema)
    def post(self, **kwargs):
        schema_serializer = ContractorRequestSchema()
        data = request.get_json(force=True)
        uuidOne = uuid.uuid1()
        contractor_id = "C_" + str(uuidOne)

        validated_data = schema_serializer.load(data)
        av = ContractorValidation()

        response = av.post_data(validated_data, type="insert", contractor_id=contractor_id)

        if (response):
            return jsonify({'Success': "Record inserted successfully."})
        else:
            return jsonify({'Error': "Record not inserted due to some errors."})


class ContractorDeleteById(MethodResource, Resource):
    @doc(description='Contractors', tags=['Contractors'])
    # @check_for_session
    # @Credentials.check_for_token
    # @marshal_with(BulkResponseQuerySchema)
    # @use_kwargs(ContractRequestSchema)
    def delete(self, contractorID):
        # get contract status from db
        result = ContractorById.get(self, contractorID)
        my_json = result.data.decode('utf8')
        decoded_data = json.loads(my_json)

        if decoded_data != 'No record is found for this ID':
            if decoded_data['ContractorID'] == contractorID:
                av = ContractorValidation()
                response = av.delete_contractor(contractorID)
                if (response):
                    return jsonify({'Success': "Record deleted successfully."})
                else:
                    return jsonify({'Error': "Record not deleted due to some errors."})
        return "No record is found to be deleted."


class ContractDeleteById(MethodResource, Resource):
    @doc(description='Contracts', tags=['Contracts'])
    # @check_for_session
    # @Credentials.check_for_token
    # @marshal_with(BulkResponseQuerySchema)
    # @use_kwargs(ContractRequestSchema)
    def delete(self, contractID):
        # get contract status from db
        result = ContractByContractId.get(self, contractID)
        my_json = result.data.decode('utf8')
        decoded_data = json.loads(my_json)
        if decoded_data != 'No data found for this ID' and decoded_data['Contract'] == contractID:
            status_value = decoded_data['ContractStatus']
            signed = re.findall(r"Signed", status_value)
            if len(signed) == 0:
                # delete obligation
                obl = GetObligationByContractId.get(self, contractID)
                my_json = obl.data.decode('utf-8')
                decoded_data = json.loads(my_json)
                if decoded_data != 'No record found for this ID':
                    obl_data = decoded_data
                    for o in obl_data:
                        obligation_id = o['obligationID'];
                        ObligationDeleteById.delete(self, obligation_id)

                cv = ContractValidation()

                response = cv.delete_contract(contractID)

                if (response):
                    return jsonify({'Success': "Record deleted successfully."})
                else:
                    return jsonify({'Error': "Record not deleted due to some errors."})
            else:
                return jsonify({'Error': "Contract can't be deleted after signed"})
        else:
            return jsonify({'Error': "Contract doesn't exist for this ID"})


class GetContractors(MethodResource, Resource):
    @doc(description='Contractors', tags=['Contractors'])
    # @check_for_session
    # @Credentials.check_for_token
    # @marshal_with(BulkResponseQuerySchema)
    def get(self):
        query = QueryEngine()
        response = json.loads(
            query.select_query_gdb(purpose=None, dataRequester=None, additionalData="contractors", contractorID=None,
                                   contractRequester=None, contractProvider=None, ))
        response = response["results"]['bindings']
        data_array = []
        if len(response) >= 1:
            for r in response:
                data = {
                    'ContractorID': r['Contractor']['value'][45:],
                    'name': r['name']['value'],
                    'phone': r['phone']['value'],
                    'email': r['email']['value'],
                    'country': r['country']['value'],
                    'territory': r['territory']['value'],
                    'address': r['address']['value'],
                }
                data_array.append(data)
            return data_array
        return "No record is found"


class GetTermTypes(MethodResource, Resource):
    @doc(description='Term Types', tags=['Term Types'])
    # @check_for_session
    # @Credentials.check_for_token
    # @marshal_with(BulkResponseQuerySchema)
    def get(self):
        query = QueryEngine()
        response = json.loads(
            query.select_query_gdb(purpose=None, dataRequester=None, additionalData="termTypes", termID=None,
                                   contractRequester=None, contractProvider=None, ))
        response = response["results"]['bindings']
        if len(response) != 0:
            term_array = []
            for r in response:
                data = {
                    'TermTypeId': r['TermType']['value'][45:],
                    'name': r['name']['value'],
                    'description': r['description']['value'],
                }
                term_array.append(data)
            return term_array
        return 'No record found for this ID'


class TermTypeById(MethodResource, Resource):
    @doc(description='Term Types', tags=['Term Types'])
    # @check_for_session
    # @Credentials.check_for_token
    # @marshal_with(BulkResponseQuerySchema)
    def get(self, termTypeID):
        query = QueryEngine()
        response = json.loads(
            query.select_query_gdb(purpose=None, dataRequester=None, additionalData="termTypeID", termTypeID=termTypeID,
                                   contractRequester=None, contractProvider=None, termID=None))
        res = response["results"]['bindings']
        if len(res) > 0:
            res = res[0]
            data = {
                'TermTypeId': res['TermType']['value'][45:],
                'name': res['name']['value'],
                'description': res['description']['value'],
            }
            return data
        return "No record available for this term type id"


class TermTypeDeleteById(MethodResource, Resource):
    @doc(description='Term Types', tags=['Term Types'])
    # @check_for_session
    # @Credentials.check_for_token
    # @marshal_with(BulkResponseQuerySchema)
    # @use_kwargs(ContractRequestSchema)
    def delete(self, termTypeID):
        # get contract status from db
        result = TermTypeById.get(self, termTypeID)
        my_json = result.data.decode('utf8')
        decoded_data = json.loads(my_json)

        if decoded_data != 'No record available for this term type id':
            if decoded_data['TermTypeId'] == termTypeID:
                av = TermTypeValidation()
                response = av.delete_term_type(termTypeID)
                if (response):
                    return jsonify({'Success': "Record deleted successfully."})
                else:
                    return jsonify({'Error': "Record not deleted due to some errors."})
            return jsonify({'Success': "Record doesn't matched."})
        return jsonify({'Success': "Record doesn't exist."})


class TermTypeCreate(MethodResource, Resource):
    @doc(description='Term Types', tags=['Term Types'])
    # @check_for_session
    # @Credentials.check_for_token
    @use_kwargs(TermTypeRequestSchema)
    def post(self, **kwargs):
        schema_serializer = TermTypeRequestSchema()
        data = request.get_json(force=True)
        uuidOne = uuid.uuid1()
        term_type_id = "Term_type_" + str(uuidOne)

        validated_data = schema_serializer.load(data)
        # print(validated_data)
        av = TermTypeValidation()
        response = av.post_data(validated_data, type="insert", term_type_id=term_type_id)
        if (response):
            return jsonify({'Success': "Record inserted successfully."})
        else:
            return jsonify({'Error': "Record not inserted due to some errors."})


class TermTypeUpdate(MethodResource, Resource):
    @doc(description='Term Types', tags=['Term Types'])
    # @check_for_session
    # @Credentials.check_for_token
    @marshal_with(BulkResponseQuerySchema)
    @use_kwargs(TermTypeUpdateSchema)
    def put(self, **kwargs):
        schema_serializer = TermTypeUpdateSchema()
        data = request.get_json(force=True)
        term_type_id = data['TermTypeId']
        # get contract status from db
        result = TermTypeById.get(self, term_type_id)
        my_json = result.data.decode('utf8')
        decoded_data = json.loads(my_json)
        if decoded_data != 'No record available for this term type id':
            if decoded_data['TermTypeId'] == term_type_id:
                validated_data = schema_serializer.load(data)
                av = TermTypeValidation()
                response = av.post_data(validated_data, type="update", term_type_id=None)
                if (response):
                    return jsonify({'Success': "Record updated successfully."})
                else:
                    return jsonify({'Error': "Record not updated due to some errors."})
            else:
                return jsonify({'Error': "Record doesn't exist ."})
        return jsonify({'Error': "Record doesn't exist ."})


class GetTerms(MethodResource, Resource):
    @doc(description='Contract Terms', tags=['Contract Terms'])
    # @check_for_session
    # @Credentials.check_for_token
    # @marshal_with(BulkResponseQuerySchema)
    def get(self):
        query = QueryEngine()
        response = json.loads(
            query.select_query_gdb(purpose=None, dataRequester=None, additionalData="terms", termID=None,
                                   contractRequester=None, contractProvider=None, ))
        response = response["results"]['bindings']
        if len(response) != 0:
            term_array = []
            for r in response:
                data = {
                    'TermId': r['Term']['value'][45:],
                    'TermTypeId': r['type']['value'][45:],
                    'ContractId': r['contract']['value'][45:],
                    'description': r['description']['value']
                }
                term_array.append(data)
            return term_array
        return 'Record does not exist'


class TermById(MethodResource, Resource):
    @doc(description='Contract Terms', tags=['Contract Terms'])
    # @check_for_session
    # @Credentials.check_for_token
    # @marshal_with(BulkResponseQuerySchema)
    def get(self, termID):
        query = QueryEngine()
        response = json.loads(
            query.select_query_gdb(purpose=None, dataRequester=None, additionalData="termID", contractID=None,
                                   contractRequester=None, contractProvider=None, termID=termID))
        res = response["results"]['bindings']
        if len(res) > 0:
            res = res[0]
            data = {
                'TermId': res['Term']['value'][45:],
                'TermTypeId': res['type']['value'][45:],
                'ContractId': res['contract']['value'][45:],
                'description': res['description']['value']
            }
            return data
        return "No record available for this term id"


class TermDeleteById(MethodResource, Resource):
    @doc(description='Contract Terms', tags=['Contract Terms'])
    # @check_for_session
    # @Credentials.check_for_token
    # @marshal_with(BulkResponseQuerySchema)
    # @use_kwargs(ContractRequestSchema)
    def delete(self, termID):
        # get contract status from db
        result = TermById.get(self, termID)
        my_json = result.data.decode('utf8')
        decoded_data = json.loads(my_json)

        if decoded_data != 'No record available for this term id':
            if decoded_data['TermId'] == termID:
                av = TermValidation()
                response = av.delete_term(termID)
                if (response):
                    return jsonify({'Success': "Record deleted successfully."})
                else:
                    return jsonify({'Error': "Record not deleted due to some errors."})
            return jsonify({'Error': "Record does not match."})
        return jsonify({'Error': "Record does not exist."})


class TermCreate(MethodResource, Resource):
    @doc(description='Contract Terms', tags=['Contract Terms'])
    # @check_for_session
    # @Credentials.check_for_token
    @use_kwargs(TermRequestSchema)
    def post(self, **kwargs):
        schema_serializer = TermRequestSchema()
        data = request.get_json(force=True)
        uuidOne = uuid.uuid1()
        term_id = "Term_" + str(uuidOne)

        validated_data = schema_serializer.load(data)
        # print(validated_data)
        av = TermValidation()
        response = av.post_data(validated_data, type="insert", term_id=term_id)
        if (response):
            return jsonify({'Success': "Record inserted successfully."})
        else:
            return jsonify({'Error': "Record not inserted due to some errors."})


class TermUpdate(MethodResource, Resource):
    @doc(description='Contract Terms', tags=['Contract Terms'])
    # @check_for_session
    # @Credentials.check_for_token
    @marshal_with(BulkResponseQuerySchema)
    @use_kwargs(TermUpdateSchema)
    def put(self, **kwargs):
        schema_serializer = TermUpdateSchema()
        data = request.get_json(force=True)
        term_id = data['TermId']
        # get contract status from db
        result = TermById.get(self, term_id)
        my_json = result.data.decode('utf8')
        decoded_data = json.loads(my_json)
        if decoded_data != 'No record available for this term id':
            if decoded_data['TermId'] == term_id:
                validated_data = schema_serializer.load(data)
                av = TermValidation()
                response = av.post_data(validated_data, type="update", term_id=None)
                if (response):
                    return jsonify({'Success': "Record updated successfully."})
                else:
                    return jsonify({'Error': "Record not updated due to some errors."})
            else:
                return jsonify({'Error': "Record doesn't exist ."})


class GetObligations(MethodResource, Resource):
    @doc(description='Contract Obligations', tags=['Contract Obligations'])
    # @check_for_session
    # @Credentials.check_for_token
    # @marshal_with(BulkResponseQuerySchema)
    def get(self):
        query = QueryEngine()
        response = json.loads(
            query.select_query_gdb(purpose=None, dataRequester=None, additionalData="obligations", termID=None,
                                   contractRequester=None, contractProvider=None, ))
        data = response["results"]['bindings']
        if len(data) != 0:

            obligation_sub_array = []
            for d in data:
                # print(d)
                obligation_id = d['Obligation']['value'][45:]

                # get contract id, term id and contractor id
                obl = ObligationById.get(self, obligation_id)
                obl_data = obl.json
                # print(obl_data)
                new_data = {
                    'obligationID': obligation_id,
                    'state': obl_data[0]['state'],
                    'description': obl_data[0]['description'],
                    'exection_date': obl_data[0]['execution_date'],
                    'end_date': obl_data[0]['end_date'],
                    'identifier': obl_data[0]['identifier'],
                }
                obligation_sub_array.append(new_data)
            if len(obligation_sub_array) != 0:
                return obligation_sub_array
        return 'No record found'


class GetObligationByContractId(MethodResource, Resource):
    @doc(description='Contract Obligations', tags=['Contract Obligations'])
    # @check_for_session
    # @Credentials.check_for_token
    # @marshal_with(BulkResponseQuerySchema)
    def get(self, contractID):
        query = QueryEngine()
        response = json.loads(
            query.select_query_gdb(purpose=None, dataRequester=None, additionalData="contractObligation",
                                   contractID=contractID,
                                   contractRequester=None, contractProvider=None, contractorID=None, termID=None
                                   ))
        data = response["results"]['bindings']
        if len(data) != 0:
            obligation_array = []
            for d in data:
                obligation_id = d['obl']['value']
                obligation_id = obligation_id[45:]
                new_data = {'obligationID': obligation_id,
                            'state': d['state']['value'][45:],
                            'description': d['obl_desc']['value'],
                            'exection_date': d['exe_date']['value'][45:],
                            'end_date': d['end_date']['value'][45:],
                            }
                obligation_array.append(new_data)
            return obligation_array
        return 'No record found for this ID'


class GetContractTerms(MethodResource, Resource):
    @doc(description='Contract Terms', tags=['Contract Terms'])
    # @check_for_session
    # @Credentials.check_for_token
    # @marshal_with(BulkResponseQuerySchema)
    def get(self, contractID):
        query = QueryEngine()
        response = json.loads(
            query.select_query_gdb(purpose=None, dataRequester=None, additionalData="contractTerms",
                                   contractID=contractID,
                                   contractRequester=None, contractProvider=None, contractorID=None, termID=None
                                   ))
        data = response["results"]["bindings"]
        if len(data) != 0:
            term_arry = []
            for d in data:
                term = d['term']['value']
                term = term[45:]
                new_data = {'termID': term, 'description': d['description']['value']}
                term_arry.append(new_data)
            return term_arry
        return 'No record found for this ID'


class GetContractContractors(MethodResource, Resource):
    @doc(description='Contract Contractors', tags=['Contract Contractors'])
    # @check_for_session
    # @Credentials.check_for_token
    # @marshal_with(BulkResponseQuerySchema)
    def get(self, contractID):
        query = QueryEngine()
        response = json.loads(
            query.select_query_gdb(purpose=None, dataRequester=None, additionalData="contractContractors",
                                   contractID=contractID,
                                   contractRequester=None, contractProvider=None, contractorID=None, termID=None
                                   ))
        data = response["results"]["bindings"]
        if len(data) != 0:
            contractor_array = []
            for d in data:
                contractor = d['contractor']['value']
                contractor = contractor[45:]
                new_data = {'contractorID': contractor,
                            'name': d['name']['value'],
                            'email': d['email']['value'],
                            'country': d['country']['value'],
                            'territory': d['territory']['value']
                            }
                contractor_array.append(new_data)
            return contractor_array
        return 'No record found for this ID'


class ObligationById(MethodResource, Resource):
    @doc(description='Contract Obligations', tags=['Contract Obligations'])
    # @check_for_session
    # @Credentials.check_for_token
    # @marshal_with(BulkResponseQuerySchema)
    def get(self, obligationID):
        query = QueryEngine()
        response = json.loads(
            query.select_query_gdb(purpose=None, dataRequester=None, additionalData="obligationID",
                                   obligationID=obligationID,
                                   contractRequester=None, contractProvider=None))
        data = response["results"]['bindings']
        # print(data)
        if len(data) != 0:
            identifier_array = []
            obligation_array = []
            for d in data:
                id = GetObligationIdentifierById.get(self, obligationID)
                id = id.json
                for i in id:
                    identifier_array.append(i)
                    new_data = {'obligationID': obligationID,
                                'state': d['state']['value'][45:],
                                'description': d['description']['value'],
                                'execution_date': d['executiondate']['value'][45:],
                                'end_date': d['enddate']['value'][45:],
                                'identifier': identifier_array
                                }
                obligation_array.append(new_data)
            if len(obligation_array) != 0:
                return obligation_array
        return 'No recrod found for this ID'


class GetObligationIdentifierById(MethodResource, Resource):
    @doc(description='Contract Obligations', tags=['Contract Obligations'])
    # @check_for_session
    # @Credentials.check_for_token
    # @marshal_with(BulkResponseQuerySchema)
    def get(self, obligationID):
        query = QueryEngine()
        response = json.loads(
            query.select_query_gdb(purpose=None, dataRequester=None, additionalData="obligationIdentifier",
                                   obligationID=obligationID,
                                   contractRequester=None, contractProvider=None))
        res = response["results"]['bindings']
        data = []
        if len(res) != 0:
            for r in res:
                a = r['identifier']['value'][45:]
                data.append(a)
            return data
        return 'No record found for this ID'


class ObligationCreate(MethodResource, Resource):
    @doc(description='Contract Obligations', tags=['Contract Obligations'])
    # @check_for_session
    # @Credentials.check_for_token
    @use_kwargs(ObligationRequestSchema)
    def post(self, **kwargs):
        schema_serializer = ObligationRequestSchema()
        data = request.get_json(force=True)
        uuidOne = uuid.uuid1()
        obligation_id = "OB_" + str(uuidOne)
        validated_data = schema_serializer.load(data)
        av = ObligationValidation()
        response = av.post_data(validated_data, type="insert", obligation_id=obligation_id)
        if (response):
            return jsonify({'Success': "Record inserted successfully."})
        return jsonify({'Error': "Record not inserted due to some errors."})

        # contract_id = data['ContractId']
        # # check contract id first
        # re = GetObligationByContractId.get(self, contract_id)
        #
        # my_json = re.data.decode('utf8')
        # decoded_data = json.loads(my_json)
        # # print(decoded_data)
        #
        # if decoded_data != 'No record found for this ID':
        #     result = decoded_data
        #     for r in result:
        #         # print(r['obligationID'])
        #         print(obligation_id)
        #         if r['obligationID'] == str(obligation_id):
        #             return jsonify({'Error': "Obligation id already exist"})
        # else:


class ObligationDeleteById(MethodResource, Resource):
    @doc(description='Contract Obligations', tags=['Contract Obligations'])
    # @check_for_session
    # @Credentials.check_for_token
    # @marshal_with(BulkResponseQuerySchema)
    # @use_kwargs(ContractRequestSchema)
    def delete(self, obligationID):
        # get contract status from db
        result = ObligationById.get(self, obligationID)
        my_json = result.data.decode('utf8')
        decoded_data = json.loads(my_json)
        if decoded_data != 'No record found for this ID':
            av = ObligationValidation()
            response = av.delete_obligation(obligationID)
            if (response):
                return jsonify({'Success': "Record deleted successfully."})
            else:
                return jsonify({'Error': "Record not deleted due to some errors."})
        return jsonify({'Success': "No record found for this ID."})


class ContractObligationUpdate(MethodResource, Resource):
    @doc(description='Contract Obligations', tags=['Contract Obligations'])
    # @check_for_session
    # @Credentials.check_for_token
    @marshal_with(BulkResponseQuerySchema)
    @use_kwargs(ObligationRequestSchema)
    def put(self, **kwargs):
        schema_serializer = ObligationRequestSchema()
        data = request.get_json(force=True)
        obligation_id = data['ObligationId']

        result = ObligationById.get(self, obligation_id)
        my_json = result.data.decode('utf8')
        decoded_data = json.loads(my_json)
        if len(decoded_data) > 0:
            validated_data = schema_serializer.load(data)
            av = ObligationValidation()
            response = av.post_data(validated_data, type="update")
            if (response):
                return response
            else:
                return jsonify({'Error': "Record not updated due to some errors."})
        else:
            return jsonify({'Error': "Record doesn't exist ."})


class ObligationStatusUpdateByObligationId(MethodResource, Resource):
    @doc(description='Contract Obligations', tags=['Contract Obligations'])
    def get(self, obligationID, contractID, contractorID, state):

        host_post = os.getenv("HOST_URI_POST")
        hostname = host_post
        userid = os.getenv("user_name")
        password = os.getenv("password")

        updated_date = date.today()
        sparql = SPARQLWrapper(hostname)
        sparql.setHTTPAuth(BASIC)
        sparql.setCredentials(userid, password)
        query = textwrap.dedent("""
         PREFIX : <http://ontologies.atb-bremen.de/smashHitCore#>
         PREFIX dct: <http://purl.org/dc/terms/>
            DELETE {{?Obligation :hasStates :hasPendingState.
                    ?Obligation :hasStates :hasViolated.
                    ?Obligation :hasStates :hasFulfilled.
                    ?Obligation :hasStates :hasInvalid.}}
            INSERT {{?Obligation :hasStates :{3}.}}
            where {{
                     ?Obligation a <http://ontologies.atb-bremen.de/smashHitCore#obligationID>;
                                 :hasStates ?state;
                     FILTER(?Obligation = :{0}) .
                    {{
                    select ?Contract
                    where{{
                    ?Contract a :contractID;
                              filter(?Contract=:{1}) .

                    }}
                    }}
                     {{
                    select ?Contractor
                    where{{
                    ?Contractor a :contractorID;
                                filter(?Contractor=:{2})
                    }}
                    }}
    }}""").format(obligationID, contractID, contractorID, state)
        sparql.setQuery(query)
        sparql.method = "POST"
        sparql.queryType = "INSERT"
        sparql.setReturnFormat('json')
        result = sparql.query()
        if str(result.response.read().decode("utf-8")) == "":
            return "Success"
        else:
            return "Fail"


class ContractStatusUpdateById(MethodResource, Resource):
    @doc(description='Contracts', tags=['Contracts'])
    def get(self, contractID, status):

        host_post = os.getenv("HOST_URI_POST")
        hostname = host_post
        userid = os.getenv("user_name")
        password = os.getenv("password")

        violation_date = date.today()
        sparql = SPARQLWrapper(hostname)
        sparql.setHTTPAuth(BASIC)
        sparql.setCredentials(userid, password)
        query = textwrap.dedent("""
         PREFIX : <http://ontologies.atb-bremen.de/smashHitCore#>
         PREFIX dct: <http://purl.org/dc/terms/>
            DELETE {{?ContractId :hasContractStatus :hasCreated.
                    ?ContractId :hasContractStatus :hasRenewed.
                    ?ContractId :hasContractStatus :hasPending.
                    ?ContractId :hasContractStatus :hasViolated.
                    ?ContractId :hasContractStatus :hasExpired.
                    ?ContractId :hasContractStatus :hasSigned.
                    ?ContractId :hasContractStatus :hasTerminated.}}
            INSERT {{?ContractId :hasContractStatus :{2}.
            ?ContractId :RevokedAtTime {0}.
            }}
             WHERE {{
             ?ContractId a <http://ontologies.atb-bremen.de/smashHitCore#contractID>.
              FILTER(?ContractId = :{1})
             }}""").format('\'{}^^xsd:dateTime\''.format(violation_date), contractID, status)

        # print(query)
        sparql.setQuery(query)
        sparql.method = "POST"
        sparql.queryType = "INSERT"
        sparql.setReturnFormat('json')
        result = sparql.query()
        if str(result.response.read().decode("utf-8")) == "":
            return "Success"
        else:
            return "Fail"


class GetContractCompliance(MethodResource, Resource):
    @doc(description='Contract Compliance', tags=['Contract Compliance'])
    # @check_for_session
    # @Credentials.check_for_token
    # @marshal_with(BulkResponseQuerySchema)
    def get(self):
        query = QueryEngine()
        response = json.loads(
            query.select_query_gdb(purpose=None, dataRequester=None, additionalData="compliance", termID=None,
                                   contractRequester=None, contractProvider=None, ))

        obligatons = response["results"]['bindings']

        # current_data = today
        # current_data = date(2022, 4, 4)
        current_data = date.today()
        contractor_id = ""
        term_id = ""

        for x in obligatons:
            identifier = x["identifier"]["value"]
            if "CONT_" in identifier:
                contract_id = identifier[45:]

                # get contract
                res_contract = ContractByContractId.get(self, contract_id)
                contract_data = res_contract.json
                contract_status = contract_data['ContractStatus']

                # get contract obligation
                res = GetObligationByContractId.get(self, contract_id)
                obligation_data = res.json
                for d in obligation_data:
                    obligation_id = d["obligationID"]
                    sdate = d["exection_date"]
                    edate = d["end_date"]
                    obl_state = d["state"]
                    obl_desc = d["description"]
                    # get contractor and term
                    ob = GetObligationIdentifierById.get(self, obligation_id)
                    identifier_data = ob.json
                    for d in identifier_data:
                        ob_data = d
                        if 'CONT_' not in ob_data:
                            if 'Term_' in ob_data:
                                term_id = ob_data
                            else:
                                contractor_id = ob_data

                    # print(contractor_id)
                    # print(term_id)

                    date_time_str = edate
                    date_time_obj = datetime.strptime(date_time_str, '%Y-%m-%d').date()

                    # print(current_data)
                    # print(date_time_obj)
                    # print(obl_state)
                    # print(contract_id)
                    # print(contract_status)

                    if current_data >= date_time_obj and obl_state == 'hasPendingState' and contract_status not in (
                            'hasViolated', 'hasTerminated'):
                        new_data = {
                            "ObligationId": obligation_id,
                            "Description": obl_desc,
                            "TermId": term_id,
                            "ContractorId": contractor_id,
                            "ContractId": contract_id,
                            "State": "hasViolated",
                            "ExecutionDate": sdate,
                            "EndDate": edate,
                        }
                        # print(new_data)
                        # update contract status
                        ContractStatusUpdateById.get(self, contract_id, 'hasViolated')
                        # update obligation
                        schema_serializer = ObligationUpdateSchema()
                        data = new_data
                        obligation_id = data['ObligationId']
                        result = ObligationById.get(self, obligation_id)
                        my_json = result.data.decode('utf8')
                        decoded_data = json.loads(my_json)
                        # print(decoded_data)

                        if decoded_data != 'No recrod found for this ID':
                            validated_data = schema_serializer.load(data)
                            av = ObligationValidation()
                            av.post_data(validated_data, type="update", obligation_id=obligation_id)

                        # Email to contractors in case of violation

                        message = 'In contract id = ' + str(
                            contract_id) + ' ' + obl_desc + ' with obligation id ' + obligation_id + \
                                  '  has been violated'
                        from_email = 'amar.tauqeer@gmail.com'
                        # get contract contractors
                        res = GetContractContractors.get(self, contract_id)
                        contractors = res.json

                        for c in contractors:
                            email = c['email']
                            server = smtplib.SMTP("smtp.gmail.com", 587)
                            server.starttls()
                            server.login(os.environ.get('MAIL_USERNAME'), os.environ.get('MAIL_PASSWORD'))
                            server.sendmail(from_email, email, message)
        return 'Success'

# class GetContractTestResult(MethodResource, Resource):
#     # @Credentials.check_for_token
#     # @marshal_with(BulkResponseQuerySchema)
#     def get(self):
#         response=ContractApiTest.test_get_all_contracts()
#         return response, 200
