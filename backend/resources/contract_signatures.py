from core.security.RsaAesDecryption import RsaAesDecrypt
from core.signature_validation.contract_signatures_validation import ContractSignatureValidation
from resources.schemas import *


class GetSignatures(MethodResource, Resource):
    @doc(description='Contract Signatures', tags=['Contract Signatures'])
    # @check_for_session
    @Credentials.check_for_token
    # @marshal_with(BulkResponseQuerySchema)
    def get(self):
        query = QueryEngine()
        response = json.loads(
            query.select_query_gdb(purpose=None, dataRequester=None, additionalData="signatures", termID=None,
                                   contractRequester=None, contractProvider=None, ))
        response = response["results"]['bindings']
        # print(response)
        if len(response) != 0:
            signature_arry = []
            for d in response:
                signatureId = d['signatureId']['value']
                # print(signature)
                # get contract and contractor
                sig = SignatureById.get(self, signatureId)
                sig_data = sig.json
                identifier = sig_data[0]['identifier']
                create_date = sig_data[0]['createDate']
                signature_text = sig_data[0]['signatureText']

                new_data = {'signatureId': signatureId, 'identifier': identifier,
                            'createDate': create_date, 'signatureText': signature_text}
                signature_arry.append(new_data)
            if len(signature_arry) != 0:
                return signature_arry
        return 'No record found for this ID'


class SignatureById(MethodResource, Resource):
    @doc(description='Contract Signatures', tags=['Contract Signatures'])
    # @check_for_session
    @Credentials.check_for_token
    # @marshal_with(BulkResponseQuerySchema)
    def get(self, signatureID):
        query = QueryEngine()
        response = json.loads(
            query.select_query_gdb(purpose=None, dataRequester=None, additionalData="signatureID",
                                   signatureID=signatureID,
                                   contractRequester=None, contractProvider=None, termID=None))
        res = response["results"]['bindings']
        # print(res)
        if len(res) != 0:
            identifier_array = []
            signature_array = []
            for d in res:
                id = GetSignatureIdentifierById.get(self, signatureID)
                id = id.json
                for i in id:
                    identifier_array.append(i)
                obj_dec = RsaAesDecrypt()
                data = {'signature_id': signatureID, 'signature': d['signatureText']['value'],
                        }
                decrypted_result = obj_dec.rsa_aes_decrypt(data)
                signature = decrypted_result[0]['signature']

                new_data = {'signatureId': signatureID,
                            'createDate': d['createDate']['value'],
                            'signatureText':  signature,#d['signatureText']['value'],
                            'identifier': identifier_array
                            }
                signature_array.append(new_data)
            if len(signature_array) != 0:
                return signature_array
        return 'No recrod found for this ID'


class SignatureDeleteById(MethodResource, Resource):
    @doc(description='Contract Signatures', tags=['Contract Signatures'])
    # @check_for_session
    @Credentials.check_for_token
    # @marshal_with(BulkResponseQuerySchema)
    # @use_kwargs(ContractRequestSchema)
    def delete(self, signatureID):
        # get contract status from db
        result = SignatureById.get(self, signatureID)
        my_json = result.data.decode('utf8')
        decoded_data = json.loads(my_json)

        if decoded_data != 'No record available for this term id':
            if decoded_data[0]['signatureId'] == signatureID:
                av = ContractSignatureValidation()
                response = av.delete_contract_signature(signatureID)
                if (response):
                    return jsonify({'Success': "Record deleted successfully."})
                else:
                    return jsonify({'Error': "Record not deleted due to some errors."})
            return jsonify({'Error': "Record does not match."})
        return jsonify({'Error': "Record does not exist."})


class ContractSignatureCreate(MethodResource, Resource):
    @doc(description='Contract Signatures', tags=['Contract Signatures'])
    # @check_for_session
    @Credentials.check_for_token
    @use_kwargs(ContractorSignaturesRequestSchema)
    def post(self, **kwargs):
        schema_serializer = ContractorSignaturesRequestSchema()
        data = request.get_json(force=True)
        uuidOne = uuid.uuid1()
        signature_id = "sig_" + str(uuidOne)

        validated_data = schema_serializer.load(data)
        # print(validated_data)
        av = ContractSignatureValidation()
        response = av.post_data(validated_data, type="insert", signature_id=signature_id)
        if response == 'Success':
            contract_obj = SignatureById.get(self, signature_id)
            contract_obj = contract_obj.json
            return contract_obj
        else:
            return jsonify({'Error': "Record not inserted due to some errors."})


class ContractSignatureUpdate(MethodResource, Resource):
    @doc(description='Contract Signatures', tags=['Contract Signatures'])
    # @check_for_session
    @Credentials.check_for_token
    @marshal_with(BulkResponseQuerySchema)
    @use_kwargs(ContractorSignaturesUpdateSchema)
    def put(self, **kwargs):
        schema_serializer = ContractorSignaturesUpdateSchema()
        data = request.get_json(force=True)
        signature_id = data['SignatureId']
        # get contract status from db
        result = SignatureById.get(self, signature_id)
        my_json = result.data.decode('utf8')
        decoded_data = json.loads(my_json)
        if decoded_data != 'No record available for this signature id':
            if decoded_data[0]['signatureId'] == signature_id:
                validated_data = schema_serializer.load(data)
                av = ContractSignatureValidation()
                response = av.post_data(validated_data, type="update", signature_id=None)
                if (response):
                    return jsonify({'Success': "Record updated successfully."})
                else:
                    return jsonify({'Error': "Record not updated due to some errors."})
            else:
                return jsonify({'Error': "Record doesn't exist ."})


class GetContractSignatures(MethodResource, Resource):
    @doc(description='Contract Signatures', tags=['Contract Signatures'])
    # @check_for_session
    @Credentials.check_for_token
    # @marshal_with(BulkResponseQuerySchema)
    def get(self, contractID):
        query = QueryEngine()
        response = json.loads(
            query.select_query_gdb(purpose=None, dataRequester=None, additionalData="contractSignatures",
                                   contractID=contractID,
                                   contractRequester=None, contractProvider=None, contractorID=None, termID=None
                                   ))
        data = response["results"]["bindings"]
        if len(data) != 0:
            identifier_array = []
            signature_array = []
            for d in data:
                signature_id = d['signatureId']['value']

                id = GetSignatureIdentifierById.get(self, signature_id)
                id = id.json
                for i in id:
                    if 'contb2c_' not in i and 'contb2b_' not in i:
                        identifier_array.append(i)
                        obj_dec = RsaAesDecrypt()
                        data = {'signature_id': signature_id, 'signature': d['signatureText']['value'],
                                }
                        decrypted_result = obj_dec.rsa_aes_decrypt(data)
                        signature = decrypted_result[0]['signature']

                        new_data = {'signatureId': signature_id,
                                    'signatureText': signature,#d['signatureText']['value'],
                                    'createDate': d['createDate']['value'],
                                    'contractorId': i
                                    }
                        signature_array.append(new_data)
            if len(signature_array) != 0:
                return signature_array
        return 'No record found for this ID'


class GetSignatureIdentifierById(MethodResource, Resource):
    @doc(description='Contract Signatures', tags=['Contract Signatures'])
    # @check_for_session
    @Credentials.check_for_token
    # @marshal_with(BulkResponseQuerySchema)
    def get(self, signatureID):
        query = QueryEngine()
        response = json.loads(
            query.select_query_gdb(purpose=None, dataRequester=None, additionalData="signatureIdentifier",
                                   signatureID=signatureID,
                                   contractRequester=None, contractProvider=None))
        res = response["results"]['bindings']
        data = []
        if len(res) != 0:
            for r in res:
                a = r['identifier']['value'][45:]
                data.append(a)
            return data
        return 'No record found for this ID'
