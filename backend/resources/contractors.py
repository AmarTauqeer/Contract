from resources.imports import *
from resources.schemas import *

class ContractorUpdate(MethodResource, Resource):
    @doc(description='Contractors', tags=['Contractors'])
    # @check_for_session
    @Credentials.check_for_token
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
    @Credentials.check_for_token
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
    @Credentials.check_for_token
    @use_kwargs(ContractorRequestSchema)
    def post(self, **kwargs):
        schema_serializer = ContractorRequestSchema()
        data = request.get_json(force=True)
        uuidOne = uuid.uuid1()
        contractor_id = "C_" + str(uuidOne)

        validated_data = schema_serializer.load(data)
        av = ContractorValidation()

        response = av.post_data(validated_data, type="insert", contractor_id=contractor_id)

        if response == 'Success':
            contract_obj = ContractorById.get(self, contractor_id)
            contract_obj = contract_obj.json
            return contract_obj
        else:
            return jsonify({'Error': "Record not inserted due to some errors."})


class ContractorDeleteById(MethodResource, Resource):
    @doc(description='Contractors', tags=['Contractors'])
    # @check_for_session
    @Credentials.check_for_token
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


class GetContractors(MethodResource, Resource):
    @doc(description='Contractors', tags=['Contractors'])
    # @check_for_session
    @Credentials.check_for_token
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
