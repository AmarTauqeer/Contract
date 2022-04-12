from core.query_processor.QueryProcessor import QueryEngine


class ContractSignatureValidation(QueryEngine):

    def __init__(self):
        super().__init__()

    def delete_contract_signature(self, signaureID):
        response = self.post_sparql(self.get_username(), self.get_password(),
                                    self.delete_contract_signature_by_id(signaureID))
        return response

    def post_data(self, validated_data, type, signature_id):
        ContractId = validated_data["ContractId"]
        ContractorId = validated_data["ContractorId"]
        CreateDate = validated_data["CreateDate"]
        Signature = validated_data["Signature"]


        if type == "insert":
            SignatureId = signature_id
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
