from core.query_processor.QueryProcessor import QueryEngine


class ObligationValidation(QueryEngine):

    def __init__(self):
        super().__init__()

    def delete_obligation(self, obligationID):
        response = self.post_sparql(self.get_username(), self.get_password(),
                                    self.delete_obligation_by_id(obligationID))
        return response

    def post_data(self, validated_data, type, obligation_id):
        Description = validated_data["Description"]
        TermId = validated_data["TermId"]
        ContractorId = validated_data["ContractorId"]
        ContractId = validated_data["ContractId"]
        State = validated_data["State"]
        ExecutionDate = validated_data["ExecutionDate"]
        EndDate = validated_data["EndDate"]

        if type == "insert":
            ObligationId = obligation_id
            respone = self.post_sparql(self.get_username(), self.get_password(),
                                       self.insert_query_obligation(ObligationId=ObligationId,
                                                              Description=Description,
                                                              TermId=TermId,
                                                              ContractorId=ContractorId,
                                                              ContractId=ContractId,
                                                              State=State,
                                                              ExecutionDate=ExecutionDate,
                                                              EndDate=EndDate,
                                                              )

                                       )
        else:
            ObligationId = validated_data["ObligationId"]
            if ObligationId != "":
                # delete from knowledge graph
                response = self.post_sparql(self.get_username(), self.get_password(),
                                            self.delete_term_by_id(ObligationId))

                # insert into kg
                respone = self.post_sparql(self.get_username(), self.get_password(),
                                           self.insert_query_obligation(ObligationId=ObligationId,
                                                                  Description=Description,
                                                                  TermId=TermId,
                                                                  ContractorId=ContractorId,
                                                                  ContractId=ContractId,
                                                                  State=State,
                                                                  ExecutionDate=ExecutionDate,
                                                                  EndDate=EndDate,
                                                                  )

                                           )
        return respone
