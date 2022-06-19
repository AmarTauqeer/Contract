# from resources.contracts import ContractByContractId
from resources.imports import *
from resources.schemas import *


class GetObligations(MethodResource, Resource):
    @doc(description='Contract Obligations', tags=['Contract Obligations'])
    # @check_for_session
    @Credentials.check_for_token
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
    @Credentials.check_for_token
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


class ObligationById(MethodResource, Resource):
    @doc(description='Contract Obligations', tags=['Contract Obligations'])
    # @check_for_session
    @Credentials.check_for_token
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
    @Credentials.check_for_token
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
    @Credentials.check_for_token
    @use_kwargs(ObligationRequestSchema)
    def post(self, **kwargs):
        schema_serializer = ObligationRequestSchema()
        data = request.get_json(force=True)
        ContractId = data["ContractId"]
        from resources.contracts import ContractByContractId
        contract_data = ContractByContractId.get(self, ContractId)
        contract_data = contract_data.json
        ContractCategory = contract_data["ContractCategory"]
        # print(ContractCategory)
        uuidOne = uuid.uuid1()
        obligation_id = "OB_" + str(uuidOne)
        validated_data = schema_serializer.load(data)
        av = ObligationValidation()
        response = av.post_data(validated_data, type="insert", obligation_id=obligation_id,
                                contract_category=ContractCategory)
        if response=='Success':
            contract_obj = ObligationById.get(self, obligation_id)
            contract_obj = contract_obj.json
            return contract_obj
        return jsonify({'Error': "Record not inserted due to some errors."})


class ObligationDeleteById(MethodResource, Resource):
    @doc(description='Contract Obligations', tags=['Contract Obligations'])
    # @check_for_session
    @Credentials.check_for_token
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
    @Credentials.check_for_token
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
    @Credentials.check_for_token
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


class ObligationStatusUpdateById(MethodResource, Resource):
    @doc(description='Contract Obligations', tags=['Contract Obligations'])
    @Credentials.check_for_token
    def get(self, obligationID, state):

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
            DELETE {{?ObligationId :hasStates :hasValid.
                    ?ObligationId :hasStates :hasPendingState.
                    ?ObligationId :hasStates :hasViolated.
                    ?ObligationId :hasStates :hasFulfilled.
                    }}
            INSERT {{?ObligationId :hasStates :{2}.
            ?ObligationId :RevokedAtTime {0}.
            }}
             WHERE {{
             ?ObligationId a <http://ontologies.atb-bremen.de/smashHitCore#obligationID>.
              FILTER(?ObligationId = :{1})
             }}""").format('\'{}^^xsd:dateTime\''.format(violation_date), obligationID, state)

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
