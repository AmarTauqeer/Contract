import os
from core.query_processor.QueryProcessor import QueryEngine
from core.security.RsaAesEncryption import RsaAesEncrypt


class TermTypeValidation(QueryEngine):

    def __init__(self):
        super().__init__()

    def delete_term_type(self, termTypeID):
        response = self.post_sparql(self.get_username(), self.get_password(),
                                    self.delete_term_type_by_id(termTypeID))
        # delete encryption file from the directory
        cwd = os.getcwd()
        file_name = cwd + '/core/security/bundle' + termTypeID + '.enc'
        # remove file from the directory
        os.remove(file_name)
        return response

    def post_data(self, validated_data, type, term_type_id):
        Name = validated_data["Name"]
        Description = validated_data["Description"]
        CreateDate = validated_data["CreateDate"]

        if type == "insert":

            TermTypeId = term_type_id
            ############## encryption ########################
            data = {'type_id': TermTypeId, 'name': Name, 'description': Description}
            obj = RsaAesEncrypt()
            encrypted_data = obj.rsa_aes_encrypt(data)

            Name = encrypted_data[1]['name']
            Description = encrypted_data[2]['description']

            ############## end encryption ########################

            respone = self.post_sparql(self.get_username(), self.get_password(),
                                       self.insert_query_term_type(TermTypeId=TermTypeId, Name=Name,
                                                                   Description=Description,
                                                                   CreateDate=CreateDate))
        else:
            TermTypeId = validated_data["TermTypeId"]
            Description = validated_data["Description"]

            ############## encryption ########################
            data = {'type_id': TermTypeId, 'name': Name, 'description': Description}
            obj = RsaAesEncrypt()
            encrypted_data = obj.rsa_aes_encrypt(data)

            Name = encrypted_data[1]['name']
            Description = encrypted_data[2]['description']

            ############## end encryption ########################

            if TermTypeId != "":
                # delete from knowledge graph
                response = self.post_sparql(self.get_username(), self.get_password(),
                                            self.delete_term_type_by_id(TermTypeId))

                # insert into kg
                respone = self.post_sparql(self.get_username(), self.get_password(),
                                           self.insert_query_term_type(TermTypeId=TermTypeId,
                                                                       Name=Name, Description=Description,
                                                                       CreateDate=CreateDate))
        return respone
