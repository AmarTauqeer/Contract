import textwrap
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
        response = response["results"]
        return response, 200


class ContractByRequester(MethodResource, Resource):
    # @check_for_session
    # @Credentials.check_for_token
    # @marshal_with(BulkResponseQuerySchema)
    def get(self, requester):
        query = QueryEngine()
        response = json.loads(
            query.select_query_gdb(purpose=None, dataRequester=None, additionalData="contractID", contractID=None,
                                   contractRequester=requester, contractProvider=None))
        response = response["results"]
        return response, 200


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
                                   contractRequester=None, contractProvider=None))
        res = jsonify(response["results"])
        res.status_code = 200
        return res


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

        if len(decoded_data['bindings']) >= 1:
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
        if len(decoded_data['bindings']) >= 1:
            status_value = decoded_data['bindings'][0]['ContractStatus']['value']
            signed = re.findall(r"Signed", status_value)
            if len(signed) == 0:
                cv = ContractValidation()

                # delete obligation
                obl = GetObligationByContractId.get(self, contractID)
                my_json = obl.data.decode('utf8')
                decoded_data = json.loads(my_json)

                if len(decoded_data['bindings']) >= 1:
                    obl_data = decoded_data['bindings']
                    for o in obl_data:
                        data = o['oid']['value'];
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
        response = response["results"]
        return response, 200


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
        res = jsonify(response["results"])
        res.status_code = 200
        return res


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
        res = jsonify(response["results"])
        res.status_code = 200
        return res


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
        res = jsonify(response["results"])
        res.status_code = 200
        return res


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
        res = jsonify(response["results"])
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

        if len(decoded_data['bindings']) >= 1:
            result = decoded_data['bindings']

            for r in result:
                ob = r['obl']['value']
                if ob == obligation_id:
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
        print(obligationID)
        # get contract status from db
        result = ObligationById.get(self, obligationID)
        my_json = result.data.decode('utf8')
        decoded_data = json.loads(my_json)
        print(len(decoded_data['bindings']))
        if len(decoded_data['bindings']) >= 1:
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


def contract_status_update_by_id(self, id):

    host_post = os.getenv("HOST_URI_POST")
    hostname = host_post
    userid= os.getenv("user_name")
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
        INSERT {{?ContractId :hasContractStatus :hasViolated.
        ?ContractId :RevokedAtTime {0}.
        }}
         WHERE {{
         ?ContractId a <http://ontologies.atb-bremen.de/smashHitCore#contractID>.
          FILTER(?ContractId = :{1})
         }}""").format('\'{}^^xsd:dateTime\''.format(violation_date), id)

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
        current_data = date(2022, 3, 28)

        for x in obligatons:
            identifier = x["identifier"]["value"]
            if "CONT" in identifier:
                contract_id = identifier[45:]
                # print(contract_id)

                # get contract
                res_contract = ContractByContractId.get(self, contract_id)
                data = res_contract.json
                contract_status = data["bindings"][0]['ContractStatus']['value']
                contract_status = contract_status[45:]
                # print(contract_status)

                # get contract obligation
                res = GetObligationByContractId.get(self, contract_id)
                data = res.json

                for d in data["bindings"]:
                    # print(d["state"]['value'])
                    oid = d["obl"]["value"]
                    sdate = d["exe_date"]["value"]
                    edate = d["end_date"]["value"]
                    obl_state = d["state"]["value"]
                    obl_state = obl_state[45:]
                    obl_desc = d["obl_desc"]["value"]

                    obligation_id = oid[45:]
                    contractor_id = ""
                    term_id = ""

                    # get contractor and term
                    ob = ObligationById.get(self, obligation_id)
                    data = ob.json
                    for d in data['bindings']:
                        ob_data = d['identifier']['value']
                        if "CONT" not in ob_data:
                            new_ob_data = ob_data
                            if "T" in new_ob_data:
                                term_id = new_ob_data
                            else:
                                contractor_id = new_ob_data

                    # print(contractor_id)
                    # print(term_id)

                    date_time_str = edate[45:]
                    date_time_obj = datetime.strptime(date_time_str, '%Y-%m-%d').date()

                    # print(current_data)
                    # print(date_time_obj)
                    # print(obl_state)

                    if current_data >= date_time_obj and obl_state == 'hasPendingState' and contract_status not in (
                            'Violated', 'Terminated'):
                        new_data = {
                            "ObligationId": obligation_id,
                            "Description": obl_desc,
                            "TermId": term_id[45:],
                            "ContractorId": contractor_id[45:],
                            "ContractId": contract_id[45:],
                            "State": "hasViolated",
                            "ExecutionDate": sdate[45:],
                            "EndDate": edate[45:],
                        }

                        # update contract status
                        status = contract_status_update_by_id(self,contract_id)


                        # update obligation
                        schema_serializer = ObligationRequestSchema()
                        data = new_data
                        obligation_id = data['ObligationId']

                        result = ObligationById.get(self, obligation_id)
                        my_json = result.data.decode('utf8')
                        decoded_data = json.loads(my_json)

                        if len(decoded_data['bindings']) >= 1:
                            # for d in decoded_data['bindings']:
                            #     print(d['state']['value'])

                            validated_data = schema_serializer.load(data)
                            av = ObligationValidation()
                            resp = av.post_data(validated_data, type="update")

                            if status and resp:
                                return "Success"
                            return "Something wrong to update contract status"


# class GetContractTestResult(MethodResource, Resource):
#     # @Credentials.check_for_token
#     # @marshal_with(BulkResponseQuerySchema)
#     def get(self):
#         response=ContractApiTest.test_get_all_contracts()
#         return response, 200
