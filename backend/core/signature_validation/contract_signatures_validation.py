import os

from core.query_processor.QueryProcessor import QueryEngine
from core.security.RsaAesEncryption import RsaAesEncrypt


class ContractSignatureValidation(QueryEngine):

    def __init__(self):
        super().__init__()

    def delete_contract_signature(self, signaureID):
        response = self.post_sparql(self.get_username(), self.get_password(),
                                    self.delete_contract_signature_by_id(signaureID))
        # delete encryption file from the directory
        cwd = os.getcwd()
        file_name = cwd + '/core/security/bundle' + signaureID + '.enc'
        # remove file from the directory
        os.remove(file_name)
        return response

    def post_data(self, validated_data, type, signature_id):
        ContractId = validated_data["ContractId"]
        ContractorId = validated_data["ContractorId"]
        CreateDate = validated_data["CreateDate"]
        Signature = validated_data["Signature"]


        if type == "insert":
            SignatureId = signature_id
            ############## encryption ########################
            data = {'signature_id': SignatureId, 'signature': Signature }
            obj = RsaAesEncrypt()
            encrypted_data = obj.rsa_aes_encrypt(data)

            Signature = encrypted_data[1]['signature']
            ############## end encryption ########################
            respone = self.post_sparql(self.get_username(), self.get_password(),
                                       self.insert_query_contract_signature(SignatureId=SignatureId,
                                                                    ContractId=ContractId,
                                                                    ContractorId=ContractorId,
                                                                    CreateDate=CreateDate,
                                                                    Signature=Signature,
                                                                    )

                                       )
        else:
            SignatureId = validated_data["SignatureId"]
            ############## encryption ########################
            data = {'signature_id': SignatureId, 'signature': Signature }
            obj = RsaAesEncrypt()
            encrypted_data = obj.rsa_aes_encrypt(data)

            Signature = encrypted_data[1]['signature']
            ############## end encryption ########################

            if SignatureId != "":
                # delete from knowledge graph
                response = self.post_sparql(self.get_username(), self.get_password(),
                                            self.delete_contract_signature_by_id(SignatureId))

                # insert into kg
                respone = self.post_sparql(self.get_username(), self.get_password(),
                                           self.insert_query_contract_signature(SignatureId=SignatureId,
                                                                    ContractId=ContractId,
                                                                    ContractorId=ContractorId,
                                                                    CreateDate=CreateDate,
                                                                    Signature=Signature,
                                                                   )

                                           )
        return respone
