from resources.imports import *
from resources.schemas import *


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
        if response=='Success':
            contract_obj = TermById.get(self, term_id)
            contract_obj = contract_obj.json
            return contract_obj
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