from core.query_processor.QueryProcessor import QueryEngine


class CompanyValidation(QueryEngine):

    def __init__(self):
        super().__init__()

    def delete_company(self, companyID):
        response = self.post_sparql(self.get_username(), self.get_password(),
                                    self.delete_company_by_id(companyID))
        return response

    def post_data(self, validated_data, type, company_id):
        Name = validated_data["Name"]
        Email = validated_data["Email"]
        Phone = validated_data["Phone"]
        Address = validated_data["Address"]
        Territory = validated_data["Territory"]
        Country = validated_data["Country"]
        Vat = validated_data["Vat"]
        CreateDate = validated_data["CreateDate"]

        if type == "insert":
            CompanyId = company_id
            respone = self.post_sparql(self.get_username(), self.get_password(),
                                       self.insert_query_company(CompanyId=CompanyId,
                                                                 Name=Name,
                                                                 Email=Email,
                                                                 Phone=Phone,
                                                                 Address=Address,
                                                                 Territory=Territory,
                                                                 Country=Country,
                                                                 Vat=Vat,
                                                                 CreateDate=CreateDate,

                                                                 )

                                       )
        else:
            CompanyId = validated_data["CompanyId"]

            if CompanyId != "":
                # delete from knowledge graph
                response = self.post_sparql(self.get_username(), self.get_password(),
                                            self.delete_company_by_id(CompanyId))

                # insert into kg
                respone = self.post_sparql(self.get_username(), self.get_password(),
                                           self.insert_query_company(CompanyId=CompanyId,
                                                                     Name=Name,
                                                                     Email=Email,
                                                                     Phone=Phone,
                                                                     Address=Address,
                                                                     Territory=Territory,
                                                                     Country=Country,
                                                                     Vat=Vat,
                                                                     CreateDate=CreateDate,
                                                                     )

                                           )
        return respone
