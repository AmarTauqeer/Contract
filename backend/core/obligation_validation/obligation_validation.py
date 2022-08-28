import os

from core.query_processor.QueryProcessor import QueryEngine
from core.security.RsaAesEncryption import RsaAesEncrypt


class ObligationValidation(QueryEngine):

    def __init__(self):
        super().__init__()

    def delete_obligation(self, obligationID):
        response = self.post_sparql(self.get_username(), self.get_password(),
                                    self.delete_obligation_by_id(obligationID))
        # delete encryption file from the directory
        cwd = os.getcwd()
        file_name = cwd + '/core/security/bundle' + obligationID + '.enc'
        # remove file from the directory
        os.remove(file_name)

        return response

    def post_data(self, validated_data, type, obligation_id, contract_category):
        Description = validated_data["Description"]
        TermId = validated_data["TermId"]
        ContractorId = validated_data["ContractorId"]
        ContractId = validated_data["ContractId"]
        ContractIdB2C = ''
        # print(ContractId)
        if contract_category == 'categoryBusinessToBusiness':
            ContractIdB2C = validated_data["ContractIdB2C"]
            # print(ContractIdB2C)
        State = validated_data["State"]
        ExecutionDate = validated_data["ExecutionDate"]
        EndDate = validated_data["EndDate"]

        # print(ContractId)

        if type == "insert":
            ObligationId = obligation_id
            ############## encryption ########################
            data = {'obligation_id': ObligationId, 'description': Description
                # , 'contractorId': ContractorId
                    }
            obj = RsaAesEncrypt()
            encrypted_data = obj.rsa_aes_encrypt(data)

            Description = encrypted_data[1]['description']
            # ContractorId = encrypted_data[2]['contractor_id']

            ############## end encryption ########################

            # print('insert')
            respone = self.post_sparql(self.get_username(), self.get_password(),
                                       self.insert_query_obligation(ObligationId=ObligationId,
                                                                    Description=Description,
                                                                    TermId=TermId,
                                                                    ContractorId=ContractorId,
                                                                    ContractId=ContractId,
                                                                    ContractIdB2C=ContractIdB2C,
                                                                    State=State,
                                                                    ExecutionDate=ExecutionDate,
                                                                    EndDate=EndDate,
                                                                    )

                                       )
        else:
            ObligationId = validated_data["ObligationId"]

            ############## encryption ########################
            data = {'obligation_id': ObligationId, 'description': Description, 'contractorId': ContractorId}
            obj = RsaAesEncrypt()
            encrypted_data = obj.rsa_aes_encrypt(data)

            Description = encrypted_data[1]['description']
            ContractorId = encrypted_data[2]['contractor_id']

            ############## end encryption ########################


            if ObligationId != "":
                # delete from knowledge graph
                response = self.post_sparql(self.get_username(), self.get_password(),
                                            self.delete_obligation_by_id(ObligationId))

                # insert into kg
                print(ContractId)
                respone = self.post_sparql(self.get_username(), self.get_password(),
                                           self.insert_query_obligation(ObligationId=ObligationId,
                                                                        Description=Description,
                                                                        TermId=TermId,
                                                                        ContractorId=ContractorId,
                                                                        ContractId=ContractId,
                                                                        ContractIdB2C=ContractIdB2C,
                                                                        State=State,
                                                                        ExecutionDate=ExecutionDate,
                                                                        EndDate=EndDate,
                                                                        )

                                           )
        return respone
