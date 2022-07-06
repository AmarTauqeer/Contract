import os

from core.query_processor.QueryProcessor import QueryEngine
from core.security.RsaAesEncryption import RsaAesEncrypt


class ContractorValidation(QueryEngine):

    def __init__(self):
        super().__init__()

    def delete_contractor(self, contractorID):
        response = self.post_sparql(self.get_username(), self.get_password(),
                                    self.delete_contractor_by_id(contractorID))

        # delete encryption file from the directory
        cwd = os.getcwd()
        file_name = cwd + '/core/security/bundle' + contractorID + '.enc'
        # remove file from the directory
        os.remove(file_name)

        return response

    def post_data(self, validated_data, type, contractor_id):
        Name = validated_data["Name"]
        Email = validated_data["Email"]
        Phone = validated_data["Phone"]
        Address = validated_data["Address"]
        Territory = validated_data["Territory"]
        Country = validated_data["Country"]
        Role = validated_data["Role"]
        Vat = validated_data["Vat"]
        CompanyId = validated_data["CompanyId"]
        CreateDate = validated_data["CreateDate"]

        if type == "insert":
            ContractorId = contractor_id
            ############## encryption ########################
            data = {'contractor_id': ContractorId, 'name': Name, 'email': Email, 'phone': Phone, \
                    'address': Address, 'country': Country, 'vat': Vat, 'territory': Territory, }
            obj = RsaAesEncrypt()
            encrypted_data = obj.rsa_aes_encrypt(data)

            Name = encrypted_data[1]['name']
            Email = encrypted_data[2]['email']
            Phone = encrypted_data[3]['phone']
            Address = encrypted_data[4]['address']
            Country = encrypted_data[5]['country']
            Vat = encrypted_data[6]['vat']
            Territory = encrypted_data[7]['territory']
            ############## end encryption ########################

            respone = self.post_sparql(self.get_username(), self.get_password(),
                                       self.insert_query_contractor(ContractorId=ContractorId,
                                                                    Name=Name,
                                                                    Email=Email,
                                                                    Phone=Phone,
                                                                    Address=Address,
                                                                    Territory=Territory,
                                                                    Country=Country,
                                                                    Role=Role,
                                                                    Vat=Vat,
                                                                    CompanyId=CompanyId,
                                                                    CreateDate=CreateDate
                                                                    )

                                       )
        else:
            ContractorId = validated_data["ContractorId"]

            ############## encryption ########################

            data = {'contractor_id': ContractorId, 'name': Name, 'email': Email, 'phone': Phone, \
                    'address': Address, 'country': Country, 'vat': Vat, 'territory': Territory, }
            obj = RsaAesEncrypt()
            encrypted_data = obj.rsa_aes_encrypt(data)

            Name = encrypted_data[1]['name']
            Email = encrypted_data[2]['email']
            Phone = encrypted_data[3]['phone']
            Address = encrypted_data[4]['address']
            Country = encrypted_data[5]['country']
            Vat = encrypted_data[6]['vat']
            Territory = encrypted_data[7]['territory']

            ############## end encryption ########################

            if ContractorId != "":
                # delete from knowledge graph
                response = self.post_sparql(self.get_username(), self.get_password(),
                                            self.delete_contractor_by_id(ContractorId))

                # insert into kg
                respone = self.post_sparql(self.get_username(), self.get_password(),
                                           self.insert_query_contractor(ContractorId=ContractorId,
                                                                        Name=Name,
                                                                        Email=Email,
                                                                        Phone=Phone,
                                                                        Address=Address,
                                                                        Territory=Territory,
                                                                        Country=Country,
                                                                        Role=Role,
                                                                        Vat=Vat,
                                                                        CompanyId=CompanyId,
                                                                        CreateDate=CreateDate
                                                                        )

                                           )
        return respone
