from resources.imports import *
from resources.schemas import *
from core.security.RsaAesDecryption import RsaAesDecrypt
from core.security.RsaAesEncryption import RsaAesEncrypt


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
            obj_dec = RsaAesDecrypt()
            term_array = []
            for r in response:
                data = {'type_id': r['termTypeId']['value'], 'name': r['name']['value'],
                        'description': r['description']['value']}
                decrypted_result = obj_dec.rsa_aes_decrypt(data)
                name = decrypted_result[0]['name']
                description = decrypted_result[1]['description']
                data = {
                    'termTypeId': r['termTypeId']['value'],
                    'name': name,#r['name']['value'],
                    'description': description,#r['description']['value'],
                    'createDate': r['createDate']['value'],
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
            obj_dec = RsaAesDecrypt()
            data = {'type_id': res['termTypeId']['value'], 'name': res['name']['value'],
                    'description': res['description']['value']}
            decrypted_result = obj_dec.rsa_aes_decrypt(data)
            name = decrypted_result[0]['name']
            description = decrypted_result[1]['description']
            data = {
                'termTypeId': res['termTypeId']['value'],
                'name': name,#res['name']['value'],
                'description': description,#res['description']['value'],
                'createDate': res['createDate']['value'],
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
            if decoded_data['termTypeId'] == termTypeID:
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
        term_type_id = "term_type_" + str(uuidOne)

        validated_data = schema_serializer.load(data)
        # print(validated_data)
        av = TermTypeValidation()
        response = av.post_data(validated_data, type="insert", term_type_id=term_type_id)
        if response == 'Success':
            contract_obj = TermTypeById.get(self, term_type_id)
            contract_obj = contract_obj.json
            return contract_obj
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
            if decoded_data['termTypeId'] == term_type_id:
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
