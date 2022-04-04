from core.query_processor.QueryProcessor import QueryEngine


class ContractorValidation(QueryEngine):

    def __init__(self):
        super().__init__()

    def delete_contractor(self, contractorID):
        response = self.post_sparql(self.get_username(), self.get_password(),
                                    self.delete_contractor_by_id(contractorID))
        return response

    def post_data(self, validated_data, type, contractor_id):
        Name = validated_data["Name"]
        Email = validated_data["Email"]
        Phone = validated_data["Phone"]
        Address = validated_data["Address"]
        Territory = validated_data["Territory"]
        Country = validated_data["Country"]
        Role = validated_data["Role"]

        if type == "insert":
            ContractorId = contractor_id
            respone = self.post_sparql(self.get_username(), self.get_password(),
                                       self.insert_query_contractor(ContractorId=ContractorId,
                                                                    Name=Name,
                                                                    Email=Email,
                                                                    Phone=Phone,
                                                                    Address=Address,
                                                                    Territory=Territory,
                                                                    Country=Country,
                                                                    Role=Role,
                                                                    )

                                       )
        else:
            ContractorId = validated_data["ContractorId"]
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
                                                                   )

                                           )
        return respone
