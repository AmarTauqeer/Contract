from core.query_processor.QueryProcessor import QueryEngine


class TermValidation(QueryEngine):

    def __init__(self):
        super().__init__()

    def delete_term(self, termID):
        response = self.post_sparql(self.get_username(), self.get_password(),
                                    self.delete_term_by_id(termID))
        return response

    def post_data(self, validated_data, type, term_id):
        TermTypeId = validated_data["TermTypeId"]
        ContractId = validated_data["ContractId"]
        Description = validated_data["Description"]
        CreateDate = validated_data["CreateDate"]

        if type == "insert":
            TermId = term_id
            respone = self.post_sparql(self.get_username(), self.get_password(),
                                       self.insert_query_term(TermId=TermId,
                                                              TermTypeId=TermTypeId,
                                                              ContractId=ContractId,
                                                              Description=Description,
                                                              CreateDate=CreateDate,
                                                              )

                                       )
        else:
            TermId = validated_data["TermId"]
            if TermId != "":
                # delete from knowledge graph
                response = self.post_sparql(self.get_username(), self.get_password(),
                                            self.delete_term_by_id(TermId))

                # insert into kg
                respone = self.post_sparql(self.get_username(), self.get_password(),
                                           self.insert_query_term(TermId=TermId,
                                                                  TermTypeId=TermTypeId,
                                                                  ContractId=ContractId,
                                                                  Description=Description,
                                                                  CreateDate=CreateDate,
                                                                  )

                                           )
        return respone
