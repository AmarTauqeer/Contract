from core.query_processor.QueryProcessor import QueryEngine


class ContractValidation(QueryEngine):

    def __init__(self):
        super().__init__()

    def list_to_query(self, data, whatfor):
        """ Convert list of data processing information to SPARQL query strings
        :input: data<list> [
        :input: whatfor<string> - SPARQL property
        :returns: SPARQL query string
        """
        querydata = ""
        for vlaue in data:
            strs = ":" + whatfor + " :" + vlaue + ";\n"
            querydata = strs + querydata
        return querydata

    def delete_contract(self, contractID):
        response = self.post_sparql(self.get_username(), self.get_password(), self.delete_contract_by_id(contractID))
        return response

    def post_data(self, validated_data, type, contract_id):
        ContractType = validated_data["ContractType"]
        Purpose = validated_data["Purpose"]
        EffectiveDate = validated_data["EffectiveDate"]
        ExecutionDate = validated_data["ExecutionDate"]
        EndDate = validated_data["EndDate"]
        Medium = validated_data["Medium"]
        ContractStatus = validated_data["ContractStatus"]
        ContractCategory = validated_data["ContractCategory"]
        ConsentId = validated_data["ConsentId"]
        if ContractCategory!='categoryBusinessToConsumer':
            ConsentId=''
        ConsiderationDescription = validated_data["ConsiderationDescription"]
        ConsiderationValue = validated_data["ConsiderationValue"]
        Contractors = validated_data["Contractors"]
        Terms = validated_data["Terms"]
        Obligations = validated_data["Obligations"]
        Signatures = validated_data["Signatures"]

        if type == "insert":
            ContractId = contract_id
            respone = self.post_sparql(self.get_username(), self.get_password(),
                                       self.insert_query(ContractId=ContractId,
                                                         ContractType=ContractType,
                                                         Purpose=Purpose,
                                                         EffectiveDate=EffectiveDate,
                                                         ExecutionDate=ExecutionDate,
                                                         EndDate=EndDate,
                                                         Medium=Medium,
                                                         ContractStatus=ContractStatus,
                                                         ContractCategory=ContractCategory,
                                                         ConsentId=ConsentId,
                                                         ConsiderationDescription=ConsiderationDescription,
                                                         ConsiderationValue=ConsiderationValue,
                                                         Contractors=self.list_to_query(Contractors, "hasContractors"),
                                                         Terms=self.list_to_query(Terms, "hasTerms"),
                                                         Obligations=self.list_to_query(Obligations, "hasObligations"),
                                                         Signatures=self.list_to_query(Signatures, "hasSignatures")
                                                         )

                                       )
        else:
            ContractId = validated_data["ContractId"]
            if ContractId != "":
                # delete from knowledge graph
                response = self.post_sparql(self.get_username(), self.get_password(),
                                            self.delete_contract_by_id(ContractId))

                # insert into kg
                respone = self.post_sparql(self.get_username(), self.get_password(),
                                           self.insert_query(ContractId=ContractId,
                                                             ContractType=ContractType,
                                                             Purpose=Purpose,
                                                             EffectiveDate=EffectiveDate,
                                                             ExecutionDate=ExecutionDate,
                                                             EndDate=EndDate,
                                                             Medium=Medium,
                                                             ContractStatus=ContractStatus,
                                                             ContractCategory=ContractCategory,
                                                             ConsentId=ConsentId,
                                                             ConsiderationDescription=ConsiderationDescription,
                                                             ConsiderationValue=ConsiderationValue,
                                                             Contractors=self.list_to_query(Contractors,
                                                                                            "hasContractors"),
                                                             Terms=self.list_to_query(Terms, "hasTerms"),
                                                             Obligations=self.list_to_query(Obligations,
                                                                                            "hasObligations"),
                                                             Signatures=self.list_to_query(Signatures, "hasSignatures")
                                                             )

                                           )
        return respone
