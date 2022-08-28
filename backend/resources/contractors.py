from core.security.RsaAesDecryption import RsaAesDecrypt
from resources.imports import *
from resources.schemas import *


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
            obj_dec = RsaAesDecrypt()
            data = {'contractor_id': res[0]['contractorId']['value'], 'name': res[0]['name']['value'],
                    'email': res[0]['email']['value'],
                    'phone': res[0]['phone']['value'],
                    'address': res[0]['address']['value'],
                    'country': res[0]['country']['value'],
                    'vat': res[0]['vat']['value'],
                    'territory': res[0]['territory']['value']}
            decrypted_result = obj_dec.rsa_aes_decrypt(data)
            name = decrypted_result[0]['name']
            email = decrypted_result[1]['email']
            phone = decrypted_result[2]['phone']
            address = decrypted_result[3]['address']
            country = decrypted_result[4]['country']
            vat = decrypted_result[5]['vat']
            territory = decrypted_result[6]['territory']

            data = {
                'contractorId': res[0]['contractorId']['value'],
                'name': name,#res[0]['name']['value'],
                'phone': phone,#res[0]['phone']['value'],
                'email': email,#res[0]['email']['value'],
                'country': country,#res[0]['country']['value'],
                'territory': territory,#res[0]['territory']['value'],
                'address': address,#res[0]['address']['value'],
                'vat': vat,#res[0]['vat']['value'],
                'companyId': res[0]['companyId']['value'][45:],
                'createDate': res[0]['createDate']['value'],
                'role': res[0]['role']['value'][45:],
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
        contractor_id = "c_" + str(uuidOne)

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
    # @Credentials.check_for_token
    # @marshal_with(BulkResponseQuerySchema)
    # @use_kwargs(ContractRequestSchema)
    def delete(self, contractorID):
        # get contract status from db
        result = ContractorById.get(self, contractorID)
        my_json = result.data.decode('utf8')
        decoded_data = json.loads(my_json)

        if decoded_data != 'No record is found for this ID':
            if decoded_data['contractorId'] == contractorID:
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
                obj_dec = RsaAesDecrypt()
                data = {'contractor_id': r['contractorId']['value'], 'name': r['name']['value'],
                        'email': r['email']['value'],
                        'phone': r['phone']['value'],
                        'address': r['address']['value'],
                        'country': r['country']['value'],
                        'vat': r['vat']['value'],
                        'territory': r['territory']['value']}
                decrypted_result = obj_dec.rsa_aes_decrypt(data)
                name = decrypted_result[0]['name']
                email = decrypted_result[1]['email']
                phone = decrypted_result[2]['phone']
                address = decrypted_result[3]['address']
                country = decrypted_result[4]['country']
                vat = decrypted_result[5]['vat']
                territory = decrypted_result[6]['territory']

                data = {
                    'contractorId': r['contractorId']['value'],
                    'name': name,#r['name']['value'],
                    'phone': phone,#r['phone']['value'],
                    'email': email,#r['email']['value'],
                    'country': country,#r['country']['value'],
                    'territory': territory,#r['territory']['value'],
                    'address': address,#r['address']['value'],
                    'vat': vat,#r['vat']['value'],
                    'companyId': r['companyId']['value'][45:],
                    'createDate': r['createDate']['value'],
                    'role': r['role']['value'][45:],

                }
                data_array.append(data)
            return data_array
        return "No record is found"
