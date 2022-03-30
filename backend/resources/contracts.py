import textwrap

import smtplib
from flask_mail import Message

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
    ObligationId = fields.String(required=True, description="Obligation ID")
    Description = fields.String(required=True, description="Description")
    TermId = fields.String(required=True, description="Term ID")
    ContractorId = fields.String(required=True, description="Contractor ID")
    ContractId = fields.String(required=True, description="Contract ID")
    State = fields.String(required=False, description="Obligation State")
    ExecutionDate = fields.Date(required=False, description="Execution Date")
    EndDate = fields.Date(required=False, description="End Date")


class ContractorRequestSchema(Schema):
    ContractorId = fields.String(required=True, description="Contractor ID")
    Name = fields.String(required=True, description="Name")
    Email = fields.String(required=False, description="Email")
    Phone = fields.String(required=False, description="Phone Number")
    Address = fields.String(required=True, description="Street Address")
    Territory = fields.String(required=False, description="Territory")
    Country = fields.String(required=False, description="Country")
    Role = fields.String(required=False, description="Role")


class TermRequestSchema(Schema):
    TermId = fields.String(required=True, description="Term ID")
    Name = fields.String(required=True, description="Name")
    Description = fields.String(required=False, description="Description")


class ContractRequestSchema(Schema):
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
            for c in contractors:
                cid = c['contractorID']
                contractor_array.append(cid)

            # get terms
            terms = GetContractTerms.get(self, contid)
            terms = terms.json

            for t in terms:
                tid = t['termID']
                term_array.append(tid)

            # get obligation
            obl = GetObligationByContractId.get(self, contid)
            obl = obl.json
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
        return all_data


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
        main_data=[]
        for r in response:
            contract_id= r['Contract']['value'][45:]
            res=ContractByContractId.get(self,contract_id)
            # print(res.json)
            data=res.json
            for d in data:
                main_data.append(d)
        return main_data, 200


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
        contractor_array = []
        term_array = []
        obligation_array = []

        for d in data:
            # get contractors
            contractors = GetContractContractors.get(self, contractID)
            contractors = contractors.json
            for c in contractors:
                cid = c['contractorID']
                contractor_array.append(cid)

            # get terms
            terms = GetContractTerms.get(self, contractID)
            terms = terms.json
            # print(terms)
            for t in terms:
                tid = t['termID']
                term_array.append(tid)

            # get obligation
            obl = GetObligationByContractId.get(self, contractID)
            obl = obl.json
            for o in obl:
                oid = o['obligationID']
                obligation_array.append(oid)

        obj = {
            'contractors': contractor_array,
            'terms': term_array,
            'obligations': obligation_array
        }
        data.append(obj)
        return data


class ContractUpdate(MethodResource, Resource):
    @doc(description='Contracts', tags=['Contracts'])
    # @check_for_session
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
        status_value = decoded_data[0]['ContractStatus']['value']
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
    @doc(description='Contracts', tags=['Contracts'])
    # @check_for_session
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

        if len(decoded_data) > 1:
            return jsonify({'Error': "Contract id already exist"})
        else:
            validated_data = schema_serializer.load(data)
            cv = ContractValidation()
            response = cv.post_data(validated_data, type="insert")
            if (response):
                return jsonify({'Success': "Record inserted successfully."})
            else:
                return jsonify({'Error': "Record not inserted due to some errors."})


class ContractorUpdate(MethodResource, Resource):
    @doc(description='Contractors', tags=['Contractors'])
    # @check_for_session
    # @Credentials.check_for_token
    @marshal_with(BulkResponseQuerySchema)
    @use_kwargs(ContractorRequestSchema)
    def put(self, **kwargs):
        schema_serializer = ContractorRequestSchema()
        data = request.get_json(force=True)
        contractor_id = data['ContractorId']
        # get contract status from db
        result = ContractorById.get(self, contractor_id)
        my_json = result.data.decode('utf8')
        decoded_data = json.loads(my_json)
        if len(decoded_data) > 0:
            validated_data = schema_serializer.load(data)
            av = ContractorValidation()
            response = av.post_data(validated_data, type="update")
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
        res = jsonify(response["results"])
        res.status_code = 200
        return res


class ContractorCreate(MethodResource, Resource):
    @doc(description='Contractors', tags=['Contractors'])
    # @check_for_session
    # @Credentials.check_for_token
    @use_kwargs(ContractorRequestSchema)
    def post(self, **kwargs):
        schema_serializer = ContractorRequestSchema()
        data = request.get_json(force=True)
        contractor_id = data['ContractorId']
        # get agent from db
        result = ContractorById.get(self, contractor_id)
        my_json = result.data.decode('utf8')
        decoded_data = json.loads(my_json)

        if len(decoded_data['bindings']) >= 1:
            return jsonify({'Error': "Contractor id already exist"})
        else:
            validated_data = schema_serializer.load(data)
            av = ContractorValidation()

            response = av.post_data(validated_data, type="insert")

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
        if len(decoded_data['bindings']) == 1:
            av = ContractorValidation()
            response = av.delete_contractor(contractorID)
            if (response):
                return jsonify({'Success': "Record deleted successfully."})
            else:
                return jsonify({'Error': "Record not deleted due to some errors."})


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
        if len(decoded_data) >= 1:
            status_value = decoded_data[0]['ContractStatus']['value']
            signed = re.findall(r"Signed", status_value)
            if len(signed) == 0:
                cv = ContractValidation()

                # delete obligation
                obl = GetObligationByContractId.get(self, contractID)
                my_json = obl.data.decode('utf8')
                decoded_data = json.loads(my_json)

                if len(decoded_data) >= 1:
                    obl_data = decoded_data
                    # print(obl_data)
                    for o in obl_data:
                        data = o['obl']['value'];
                        data = data[45:]
                        ObligationDeleteById.delete(self, data)

                response = cv.delete_contract(contractID)

                if (response):
                    return jsonify({'Success': "Record deleted successfully."})
                else:
                    return jsonify({'Error': "Record not deleted due to some errors."})
            else:
                return jsonify({'Error': "Contract can't be deleted after signed"})
        else:
            return jsonify({'Error': "Contract doesn't exist"})


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
        response = response["results"]
        return response, 200


class GetTerms(MethodResource, Resource):
    @doc(description='Terms', tags=['Terms'])
    # @check_for_session
    # @Credentials.check_for_token
    # @marshal_with(BulkResponseQuerySchema)
    def get(self):
        query = QueryEngine()
        response = json.loads(
            query.select_query_gdb(purpose=None, dataRequester=None, additionalData="terms", termID=None,
                                   contractRequester=None, contractProvider=None, ))
        response = response["results"]
        return response, 200


class TermById(MethodResource, Resource):
    @doc(description='Terms', tags=['Terms'])
    # @check_for_session
    # @Credentials.check_for_token
    # @marshal_with(BulkResponseQuerySchema)
    def get(self, termID):
        query = QueryEngine()
        response = json.loads(
            query.select_query_gdb(purpose=None, dataRequester=None, additionalData="termID", contractID=None,
                                   contractRequester=None, contractProvider=None, termID=termID))
        res = jsonify(response["results"])
        res.status_code = 200
        return res


class TermDeleteById(MethodResource, Resource):
    @doc(description='Terms', tags=['Terms'])
    # @check_for_session
    # @Credentials.check_for_token
    # @marshal_with(BulkResponseQuerySchema)
    # @use_kwargs(ContractRequestSchema)
    def delete(self, termID):
        # get contract status from db
        result = TermById.get(self, termID)
        my_json = result.data.decode('utf8')
        decoded_data = json.loads(my_json)
        if len(decoded_data['bindings']) == 1:
            av = TermValidation()
            response = av.delete_term(termID)
            if (response):
                return jsonify({'Success': "Record deleted successfully."})
            else:
                return jsonify({'Error': "Record not deleted due to some errors."})


class TermCreate(MethodResource, Resource):
    @doc(description='Terms', tags=['Terms'])
    # @check_for_session
    # @Credentials.check_for_token
    @use_kwargs(TermRequestSchema)
    def post(self, **kwargs):
        schema_serializer = TermRequestSchema()
        data = request.get_json(force=True)
        term_id = data['TermId']
        # get agent from db
        result = TermById.get(self, term_id)
        my_json = result.data.decode('utf8')
        decoded_data = json.loads(my_json)

        if len(decoded_data['bindings']) >= 1:
            return jsonify({'Error': "Term id already exist"})
        else:
            validated_data = schema_serializer.load(data)
            av = TermValidation()

            response = av.post_data(validated_data, type="insert")

            if (response):
                return jsonify({'Success': "Record inserted successfully."})
            else:
                return jsonify({'Error': "Record not inserted due to some errors."})


class TermUpdate(MethodResource, Resource):
    @doc(description='Terms', tags=['Terms'])
    # @check_for_session
    # @Credentials.check_for_token
    @marshal_with(BulkResponseQuerySchema)
    @use_kwargs(TermRequestSchema)
    def put(self, **kwargs):
        schema_serializer = TermRequestSchema()
        data = request.get_json(force=True)
        term_id = data['TermId']
        # get contract status from db
        result = TermById.get(self, term_id)
        my_json = result.data.decode('utf8')
        decoded_data = json.loads(my_json)
        if len(decoded_data) > 0:
            validated_data = schema_serializer.load(data)
            av = TermValidation()
            response = av.post_data(validated_data, type="update")
            if (response):
                return response
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
        obligation_array = [{'Obligations': obligation_sub_array}]
        # print(obligation_array)
        return obligation_array


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
        term_arry = []
        for d in data:
            term = d['term']['value']
            term = term[45:]
            new_data = {'termID': term, 'description': d['description']['value']}
            term_arry.append(new_data)
        return term_arry


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
        identifier_array = []
        obligation_array = []
        for d in data:
            id = GetObligationIdentifierById.get(self, obligationID)
            id = id.json
            for i in id:
                ids = i['identifier']['value'][45:]
                identifier_array.append(ids)

            new_data = {'obligationID': obligationID,
                        'state': d['state']['value'][45:],
                        'description': d['description']['value'],
                        'execution_date': d['executiondate']['value'][45:],
                        'end_date': d['enddate']['value'][45:],
                        'identifier': identifier_array
                        }
            obligation_array.append(new_data)
        return obligation_array


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
        res = jsonify(response["results"]['bindings'])
        # print(res)
        res.status_code = 200
        return res


class ObligationCreate(MethodResource, Resource):
    @doc(description='Contract Obligations', tags=['Contract Obligations'])
    # @check_for_session
    # @Credentials.check_for_token
    @use_kwargs(ObligationRequestSchema)
    def post(self, **kwargs):
        schema_serializer = ObligationRequestSchema()
        data = request.get_json(force=True)
        obligation_id = data['ObligationId']
        contract_id = data['ContractId']
        # get agent from db
        # check contract id first
        re = GetObligationByContractId.get(self, contract_id)

        my_json = re.data.decode('utf8')
        decoded_data = json.loads(my_json)

        # print(decoded_data)

        if len(decoded_data) >= 1:
            result = decoded_data

            for r in result:
                ob = r['obligations']
                for o in ob:
                    print(o['obligationID'])
                    print(obligation_id)
                    if o['obligationID'] == obligation_id:
                        return jsonify({'Error': "Obligation id already exist"})
                    else:
                        validated_data = schema_serializer.load(data)
                        av = ObligationValidation()

                        response = av.post_data(validated_data, type="insert")

                        if (response):
                            return jsonify({'Success': "Record inserted successfully."})
                        else:
                            return jsonify({'Error': "Record not inserted due to some errors."})
        else:
            validated_data = schema_serializer.load(data)
            av = ObligationValidation()

            response = av.post_data(validated_data, type="insert")

            if (response):
                return jsonify({'Success': "Record inserted successfully."})
            else:
                return jsonify({'Error': "Record not inserted due to some errors."})


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
        if len(decoded_data) >= 1:
            av = ObligationValidation()
            response = av.delete_obligation(obligationID)
            if (response):
                return jsonify({'Success': "Record deleted successfully."})
            else:
                return jsonify({'Error': "Record not deleted due to some errors."})


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

    def get(self, obligationID,contractID,contractorID,state):

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
                    ?Obligation :hasStates :hasFulfilled.}}
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
    }}""").format(obligationID,contractID,contractorID,state)
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

    def get(self, contractID,status):

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
                    ?ContractId :hasContractStatus :hasPending.}}
            INSERT {{?ContractId :hasContractStatus :{2}.
            ?ContractId :RevokedAtTime {0}.
            }}
             WHERE {{
             ?ContractId a <http://ontologies.atb-bremen.de/smashHitCore#contractID>.
              FILTER(?ContractId = :{1})
             }}""").format('\'{}^^xsd:dateTime\''.format(violation_date), contractID,status)

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
        # current_data = date(2022, 4, 1)
        current_data = date.today()
        contractor_id = ""
        term_id = ""

        for x in obligatons:
            identifier = x["identifier"]["value"]
            if "CONT" in identifier:
                contract_id = identifier[45:]

                # get contract
                res_contract = ContractByContractId.get(self, contract_id)
                data = res_contract.json
                contract_status = data[0]['ContractStatus']['value']
                contract_status = contract_status[45:]

                # get contract obligation
                res = GetObligationByContractId.get(self, contract_id)
                data = res.json

                for d in data:
                    oid = d["obligationID"]
                    sdate = d["exection_date"]
                    edate = d["end_date"]
                    obl_state = d["state"]
                    obl_desc = d["description"]
                    obligation_id = oid

                    # get contractor and term
                    ob = GetObligationIdentifierById.get(self, obligation_id)
                    data = ob.json
                    for d in data:
                        # print(d)
                        ob_data = d['identifier']['value'][45:]
                        if 'CONT' not in ob_data:
                            if 'T' in ob_data:
                                term_id = ob_data
                            else:
                                contractor_id = ob_data
                    # print(contractor_id)
                    # print(term_id)

                    date_time_str = edate
                    date_time_obj = datetime.strptime(date_time_str, '%Y-%m-%d').date()
                    #
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
                        re=ContractStatusUpdateById(self, contract_id,contract_status)
                        # update obligation
                        schema_serializer = ObligationRequestSchema()
                        data = new_data
                        obligation_id = data['ObligationId']
                        result = ObligationById.get(self, obligation_id)
                        my_json = result.data.decode('utf8')
                        decoded_data = json.loads(my_json)

                        if len(decoded_data) >= 1:
                            validated_data = schema_serializer.load(data)
                            av = ObligationValidation()
                            resp = av.post_data(validated_data, type="update")

                        # Email to contractors in case of violation

                        message = 'In contract id = ' + str(contract_id) + ' ' + obl_desc + '  is violated'
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
