import json
from SPARQLWrapper import JSON


class HelperContract:

    def contract_exists(self, contract):
        try:
            contract_data = contract["results"]["bindings"][0]["ContractId"]["value"]
            # print(contract_data)
            if len(contract_data.strip()) > 2:
                return True
            return False
        except:
            return False

    def function_map(self, name):
        """ Map to actual function
        :param name: name which function to map
        :return: function name
        """
        mapfunc = {
            "get_all_contracts": self.get_all_contracts,
            "get_contract_by_requester": self.get_contract_by_requester,
            "get_contract_by_provider": self.get_contract_by_provider,
            "get_contract_by_id": self.get_contract_by_id,
            "get_contractor_by_id": self.get_contractor_by_id,
            "get_all_contractors": self.get_all_contractors,
            "get_all_terms": self.get_all_terms,
            "get_term_by_id": self.get_term_by_id,
            "get_obligation_by_id": self.get_obligation_by_id,
            "get_all_obligations": self.get_all_obligations,
            "get_contract_obligations": self.get_contract_obligations,
            "get_contract_terms": self.get_contract_terms,
            "get_contract_contractors": self.get_contract_contractors,
        }
        return mapfunc[name]

    def list_to_query(self, data, whatfor):
        """ Convert list to query
        :input: list
        :returns: SPARQL query string
        """
        querydata = ""
        for vlaue in data:
            strs = ":" + whatfor + " :" + vlaue + ";\n"
            querydata = strs + querydata
        return querydata

    def which_query(self, purpose=None, dataRequester=None, additionalData=None, contractID=None,
                    contractRequester=None, contractProvider=None, contractorID=None, termID=None, obligationID=None
                    ):
        """ Define mapping to appropriate function for query generation based on input
        :param purpose:
        :param dataRequester:
        :param additionalData:
        :param contractId:
        :param contractRequester:
        :param contractProvider:
        :return: <dict>
        """

        if additionalData == "bcontractId":
            return dict({"map": "get_all_contracts"})

        if additionalData == "contractID" and contractRequester is not None:
            return dict({"map": "get_contract_by_requester", "arg": contractRequester})

        if additionalData == "contractID" and contractProvider is not None:
            return dict({"map": "get_contract_by_provider", "arg": contractProvider})

        if additionalData == "contractID" and contractID is not None:
            return dict({"map": "get_contract_by_id", "arg": contractID})

        if additionalData == "contractors":
            return dict({"map": "get_all_contractors"})

        if additionalData == "contractorID" and contractorID is not None:
            return dict({"map": "get_contractor_by_id", "arg": contractorID})

        if additionalData == "terms":
            return dict({"map": "get_all_terms"})

        if additionalData == "obligations":
            return dict({"map": "get_all_obligations"})

        if additionalData == "termID" and termID is not None:
            return dict({"map": "get_term_by_id", "arg": termID})

        if additionalData == "contractObligation" and contractID is not None:
            return dict({"map": "get_contract_obligations", "arg": contractID})

        if additionalData == "contractTerms" and contractID is not None:
            return dict({"map": "get_contract_terms", "arg": contractID})

        if additionalData == "contractContractors" and contractID is not None:
            return dict({"map": "get_contract_contractors", "arg": contractID})

        if additionalData == "obligationID" and obligationID is not None:
            return dict({"map": "get_obligation_by_id", "arg": obligationID})

    def select_query_gdb(self, purpose=None, dataRequester=None, additionalData=None, contractID=None,
                         contractRequester=None, contractProvider=None, contractorID=None, termID=None,
                         obligationID=None):

        sparql_inits = self.init_sparql(
            self.HOST_URI, self.get_username(), self.get_password())

        which_query_return = self.which_query(purpose, dataRequester, additionalData, contractID,
                                              contractRequester, contractProvider, contractorID, termID,obligationID)

        if ("arg" in which_query_return.keys()):
            sparql_inits.setQuery(self.function_map(
                which_query_return["map"])(which_query_return["arg"]))
        else:
            sparql_inits.setQuery(self.function_map(
                which_query_return["map"])())

        sparql_inits.setReturnFormat(JSON)
        results = sparql_inits.query().convert()
        return json.dumps(results)
