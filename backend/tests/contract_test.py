import unittest
import requests
from werkzeug.debug import Console


# from resources.contracts import ContractStatusUpdateById


class ContractApiTest(unittest.TestCase):
    # base url
    # CONTRACT_URL = "https://actool.contract.sti2.at/contract/"
    CONTRACT_URL = "http://172.25.7.73:5000/contract/"
    term_type_data = {
        "Description": "Data sharing in smashHit based on UC1 and UC2",
        "Name": "Data sharing in smashHit",
        "CreateDate":"2022-09-07T18:45:05.054Z",
    }
    term_type_data_update = {
        "Description": "Data sharing in smashHit based on UC1 and UC2",
        "Name": "updated Data sharing in smashHit",
        "TermTypeId": "term_type_8cdb028c-2e96-11ed-be7d-3f8589292a29",
        "CreateDate":"2022-09-07T18:45:05.054Z",
    }

    term_data = {
        "CreateDate": "2022-09-07 10:19:49.414000+00:00",
        "Description": "SmashHit data sharing term",
        "Obligations": [
            "ob_c115e70a-2e97-11ed-be7d-3f8589292a29",
            "ob_d1cf3f7e-2e97-11ed-be7d-3f8589292a29"
        ],
        "TermTypeId": "term_type_8cdb028c-2e96-11ed-be7d-3f8589292a29",
    }
    term_data_update = {
        "Description": "updated SmashHit data sharing term",
        "TermId": "term_b3dfd144-2e98-11ed-be7d-3f8589292a29",
        "Obligations": [
            "ob_c115e70a-2e97-11ed-be7d-3f8589292a29",
            "ob_d1cf3f7e-2e97-11ed-be7d-3f8589292a29"
        ],
        "TermTypeId": "term_type_8cdb028c-2e96-11ed-be7d-3f8589292a29",
        "CreateDate": "2022-09-07 10:19:49.414000+00:00",
    }

    contractor_data = {
        "Name": "Amar Tauqeer",
        "Email": "amar.tauqeer@hotmail.com",
        "Phone": "004368864133065",
        "Address": "Techniker strasse 7/008 6020 Innsbruck Austria",
        "Country": "Austria",
        "Territory": "Innsbruck",
        "Role": "DataSubject",
        "Vat": "3333333",
        "CompanyId": "cm_c487000a-2851-11ed-ae8f-f11f24693005",
        "CreateDate": "2022-09-07 12:25:37.232900",
    }

    contractor_data_update = {
        "ContractorId": "c_6a094420-2e97-11ed-be7d-3f8589292a29",
        "Name": "Amar Tauqeer",
        "Email": "amar.tauqeer@hotmail.com",
        "Phone": "004368864133065",
        "Address": "Techniker strasse 7/008 6020 Innsbruck Austria",
        "Country": "Austria",
        "Territory": "Innsbruck",
        "Role": "DataSubject",
        "Vat": "3333333",
        "CompanyId": "cm_c487000a-2851-11ed-ae8f-f11f24693005",
        "CreateDate": "2022-09-07 12:25:37.232900",
    }

    contractor_signature_data = {
        "ContractorId": "c_356d371c-2e97-11ed-be7d-3f8589292a29",
        "CreateDate": "2022-09-07 10:36:08.668000+00:00",
        "Signature": "Amar Tauqeer",
    }

    contractor_signature_data_update = {
        "SignatureId": "sig_2ff1e1bc-2e00-11ed-9d66-0242ac150002",
        "ContractorId": "c_356d371c-2e97-11ed-be7d-3f8589292a29",
        "CreateDate": "2022-09-07 10:36:08.668000+00:00",
        "Signature": "Amar Tauqeer",
    }

    obligation_data = {
        "ContractIdB2C": "",
        "ContractorId": "c_356d371c-2e97-11ed-be7d-3f8589292a29",
        "Description": "The Data Subject consents to the collection and processing of his or her connected car \
        data for the purposes described as: a. - For providing pricing and underwrite insurance policies \
        (known as a UBI Policy). - For checking the identities of people applying for policies and prevent \
        fraud. b. The connected car data shall be processed for a time-period of 10 months at a maximum starting \
        from the date this agreement is signed. c. The Data Subject reserves the right to withdraw this consent \
        at any time by notifying the Data Controller. After such a notification, the Data Controller shall no \
        longer process the data. d. In the event that the Data Controller (LexisNexis) stops the processing of \
        the connected car data, the Data Controller shall inform the Data Subject and any other party in \
        possession of the connected car data that the data processing has stopped.",
        "ExecutionDate": "2022-09-07 10:25:52.749000+00:00",
        "EndDate": "2023-07-07 10:25:52.749000+00:00",
        "FulFillmentDate": "2023-09-07 10:25:52.749000+00:00",
        "State": "hasPendingState",
    }

    contract_data = {
        "ConsentId": "",
        "ConsiderationDescription": "data sharing between Amar Tauqeer and LexisNexis",
        "ConsiderationValue": "200",
        "ContractCategory": "categoryBusinessToConsumer",
        "ContractStatus": "statusCreated",
        "ContractType": "written",
        "Contractors": [
            "c_356d371c-2e97-11ed-be7d-3f8589292a29",
            "c_6a094420-2e97-11ed-be7d-3f8589292a29"
        ],
        "EffectiveDate": "2022-09-07 10:38:07.617000+00:00",
        "EndDate": "2023-07-07 10:38:07.617000+00:00",
        "ExecutionDate": "2022-09-07 10:38:07.617000+00:00",
        "Medium": "online",
        "Purpose": "data sharing between Amar Tauqeer and LexisNexis",
        "Signatures": [
            "sig_0d930c10-2e99-11ed-be7d-3f8589292a29",
            "sig_1c5e38e6-2e99-11ed-be7d-3f8589292a29"
        ],
        "Terms": [
            "term_b3dfd144-2e98-11ed-be7d-3f8589292a29"
        ],
    }

    contract_update_data = {
        "ConsentId": "",
        "ConsiderationDescription": "data sharing between Amar Tauqeer and LexisNexis",
        "ConsiderationValue": "200",
        "ContractCategory": "categoryBusinessToConsumer",
        "ContractId": "contb2c_40ae43da-2e9e-11ed-be7d-3f8589292a29",
        "ContractStatus": "statusUpdated",
        "ContractType": "written",
        "Contractors": [
            "c_356d371c-2e97-11ed-be7d-3f8589292a29",
            "c_6a094420-2e97-11ed-be7d-3f8589292a29"
        ],
        "EffectiveDate": "2022-09-07 10:38:07.617000+00:00",
        "EndDate": "2023-07-07 10:38:07.617000+00:00",
        "ExecutionDate": "2022-09-07 10:38:07.617000+00:00",
        "Medium": "online",
        "Purpose": "data sharing between Amar Tauqeer and LexisNexis",
        "Signatures": [
            "sig_0d930c10-2e99-11ed-be7d-3f8589292a29",
            "sig_1c5e38e6-2e99-11ed-be7d-3f8589292a29"
        ],
        "Terms": [
            "term_b3dfd144-2e98-11ed-be7d-3f8589292a29"
        ],
    }

    # /******************************************************** contracts ***************************/
    # get all contracts
    def test_get_all_contracts(self):
        r = requests.get(ContractApiTest.CONTRACT_URL + "list_of_contracts/")
        self.assertEqual(r.status_code, 200)

    # get contract by contractor
    def test_get_contract_by_contractor(self):
        contractor = 'c_356d371c-2e97-11ed-be7d-3f8589292a29'
        r = requests.get(ContractApiTest.CONTRACT_URL +
                         "byContractor/{}".format(contractor))
        self.assertEqual(r.status_code, 200)

    # get contract by contract id
    def test_get_contract_by_id(self):
        contractid = 'contb2c_40ae43da-2e9e-11ed-be7d-3f8589292a29'
        r = requests.get(ContractApiTest.CONTRACT_URL +
                         "byContract/{}".format(contractid))
        self.assertEqual(r.status_code, 200)

    # contract creation
    def test_new_contract(self):
        r = requests.post(ContractApiTest.CONTRACT_URL +
                          "create/", json=ContractApiTest.contract_data)
        self.assertEqual(r.status_code, 200)

    # contract audit
    def test_update_contract(self):
        r = requests.put(ContractApiTest.CONTRACT_URL +
                         "update/", json=ContractApiTest.contract_update_data)
        self.assertEqual(r.status_code, 200)

    # /******************************************************** end contracts ***************************/

    # /******************************************************** contractors ***************************/
    # get all contractors
    def test_get_all_contractors(self):
        r = requests.get(ContractApiTest.CONTRACT_URL + "contractors/")
        self.assertEqual(r.status_code, 200)

    # get contractor by id
    def test_get_contractor_by_id(self):
        contractorid = 'c_356d371c-2e97-11ed-be7d-3f8589292a29'
        r = requests.get(ContractApiTest.CONTRACT_URL +
                         "contractor/{}".format(contractorid))
        self.assertEqual(r.status_code, 200)

    # get contract contractor
    def test_get_contract_contractor(self):
        contractid = 'contb2c_40ae43da-2e9e-11ed-be7d-3f8589292a29'
        r = requests.get(ContractApiTest.CONTRACT_URL +
                         "contractors/{}".format(contractid))
        self.assertEqual(r.status_code, 200)

    # new contractor
    def test_new_contractor(self):
        r = requests.post(ContractApiTest.CONTRACT_URL +
                          "contractor/create/", json=ContractApiTest.contractor_data)
        self.assertEqual(r.status_code, 200)

    # update contractor
    def test_update_contractor(self):
        r = requests.put(ContractApiTest.CONTRACT_URL +
                         "contractor/update/", json=ContractApiTest.contractor_data_update)
        self.assertEqual(r.status_code, 200)

    # /******************************************************** end contractors ***************************/

    # /******************************************************** term types ***************************/
    # get all term types
    def test_get_all_term_types(self):
        r = requests.get(ContractApiTest.CONTRACT_URL + "term/types")
        self.assertEqual(r.status_code, 200)

    # get term type by id
    def test_get_term_type_by_id(self):
        term_type_id = 'term_type_8cdb028c-2e96-11ed-be7d-3f8589292a29'
        r = requests.get(ContractApiTest.CONTRACT_URL +
                         "termType/{}".format(term_type_id))
        self.assertEqual(r.status_code, 200)

    # new term type
    def test_new_term_type(self):
        r = requests.post(ContractApiTest.CONTRACT_URL +
                          "term/type/create/", json=ContractApiTest.term_type_data)
        self.assertEqual(r.status_code, 200)

    # update term type
    def test_update_term_type(self):
        r = requests.put(ContractApiTest.CONTRACT_URL +
                         "term/type/update/", json=ContractApiTest.term_type_data_update)
        self.assertEqual(r.status_code, 200)
    #
    # # delete term type by id
    # def test_delete_term_type_by_id(self):
    #     id = 'term_type_2dd5f504-2dd7-11ed-bb84-0242ac150002'
    #     r = requests.delete(ContractApiTest.CONTRACT_URL +
    #                         "term/type/delete/{}/".format(id))
    #     self.assertEqual(r.status_code, 200)

    # /******************************************************** end term types ***************************/

    # /******************************************************** contract term ***************************/
    # get term by contract id
    def test_get_term_by_contract_id(self):
        contract_id = 'contb2c_40ae43da-2e9e-11ed-be7d-3f8589292a29'
        r = requests.get(ContractApiTest.CONTRACT_URL +
                         "term/{}".format(contract_id))
        self.assertEqual(r.status_code, 200)

    # new contract term
    def test_new_contract_term(self):
        r = requests.post(ContractApiTest.CONTRACT_URL +
                          "term/create/", json=ContractApiTest.term_data)
        self.assertEqual(r.status_code, 200)

    # update contract term
    def test_update_contract_term(self):
        r = requests.put(ContractApiTest.CONTRACT_URL +
                         "term/update/", json=ContractApiTest.term_data_update)
        self.assertEqual(r.status_code, 200)
    #
    # # delete contract term by contract id
    # def test_delete_contract_term_by_id(self):
    #     id = 'term_dd2367d4-2de2-11ed-b985-0242ac150002'
    #     r = requests.delete(ContractApiTest.CONTRACT_URL +
    #                         "contract/term/delete/{}/".format(id))
    #     self.assertEqual(r.status_code, 200)

    # /******************************************************** end contract term ***************************/

    # /******************************************************** contract obligation ***************************/
    # get all obligations
    def test_get_all_obligations(self):
        r = requests.get(ContractApiTest.CONTRACT_URL + "obligations/")
        self.assertEqual(r.status_code, 200)

    # get obligation by id
    def test_get_obligation_id(self):
        obligation_id = 'ob_c115e70a-2e97-11ed-be7d-3f8589292a29'
        r = requests.get(ContractApiTest.CONTRACT_URL +
                         "obligation/{}".format(obligation_id))
        self.assertEqual(r.status_code, 200)

    # get obligation by id
    def test_get_obligation_by_id(self):
        obligation_id = 'ob_c115e70a-2e97-11ed-be7d-3f8589292a29'
        r = requests.get(ContractApiTest.CONTRACT_URL +
                         "obligation/{}".format(obligation_id))
        self.assertEqual(r.status_code, 200)

    # new contract obligation
    # def test_new_contract_obligation(self):
    #     r = requests.post(ContractApiTest.CONTRACT_URL +
    #                       "obligation/create/", json=ContractApiTest.obligation_data)
    #     self.assertEqual(r.status_code, 200)

    # delete obligation by id
    # def test_delete_obligation_by_id(self):
    #     id = 'ob_08da59e4-2dfe-11ed-9351-0242ac150002'
    #     r = requests.delete(ContractApiTest.CONTRACT_URL +
    #                         "obligation/delete/{}/".format(id))
    #     self.assertEqual(r.status_code, 200)

    # /******************************************************** end contract obligation ***************************/

    # /******************************************************** contract signature ***************************/
    # get all signatures
    def test_get_all_signatures(self):
        r = requests.get(ContractApiTest.CONTRACT_URL + "signatures/")
        self.assertEqual(r.status_code, 200)

    # get signatures by contractid
    def test_get_signatures_by_contractid(self):
        contractid = 'contb2c_40ae43da-2e9e-11ed-be7d-3f8589292a29'
        r = requests.get(ContractApiTest.CONTRACT_URL +
                         "signatures/{}".format(contractid))
        self.assertEqual(r.status_code, 200)

    # get signatures by id
    def test_get_signatures_by_id(self):
        signatureid = 'sig_0d930c10-2e99-11ed-be7d-3f8589292a29'
        r = requests.get(ContractApiTest.CONTRACT_URL +
                         "/signature/{}".format(signatureid))
        self.assertEqual(r.status_code, 200)

    # /******************************************************** end contract signature ***************************/

    # /******************************************************** contract compliance ***************************/

    # handle single business to business contract without consent

    def test_b2b_without_consent(self):
        current_date = "2023-09-06"

        b2b_contract = "contb2b_e45dc546-2e9e-11ed-be7d-3f8589292a29"
        b2b_contract_status = "statusCreated"

        obligation_state = "statePending"
        obligation_end_date = "2023-07-06"
        obligation_id = "ob_1e5293a0-2e98-11ed-be7d-3f8589292a29"

        if current_date > obligation_end_date and obligation_state == 'statePending' and b2b_contract_status not in (
                'statusViolated', 'statusTerminated', 'statusExpired'):
            expected_status = "statusViolated"
            expected_obligation_state = "stateViolated"

            r = requests.get(ContractApiTest.CONTRACT_URL +
                             "/status/{}/{}/".format(b2b_contract, expected_status))
            self.assertEqual(r.status_code, 200)

            r = requests.get(ContractApiTest.CONTRACT_URL +
                             "/obligation/states/{}/{}/".format(obligation_id, expected_obligation_state))
            self.assertEqual(r.status_code, 200)

    #  handle single business to consumer contract without consent
    def test_b2c_without_consent(self):
        # required information
        current_date = "2023-09-06"
        b2c_contract = "contb2c_40ae43da-2e9e-11ed-be7d-3f8589292a29"
        b2c_contract_status = "statusCreated"
        obligation_state = "statePending"
        obligation_end_date = "2023-07-06"
        obligation_id = "ob_c115e70a-2e97-11ed-be7d-3f8589292a29"
        # condition
        if current_date > obligation_end_date and obligation_state == 'statePending' and b2c_contract_status not in (
                'statusViolated', 'statusTerminated', 'statusExpired'):
            print('b2c without consent')
            # update the contract status and obligation state
            r = requests.get(ContractApiTest.CONTRACT_URL +
                             "/status/{}/{}/".format(b2c_contract, "statusExpired"))
            self.assertEqual(r.status_code, 200)

            r = requests.get(ContractApiTest.CONTRACT_URL +
                             "/obligation/states/{}/{}/".format(obligation_id, "stateInvalid"))
            self.assertEqual(r.status_code, 200)

    # handle  business to consumer and business to business contract based on consent
    def test_b2b_b2c_with_consent(self):
        current_date = "2023-09-06"
        # get consent state from b2c
        consent_id = "0001"
        consent_state = "Invalid"

        b2b_contract = "contb2b_bfcff2dc-2ed3-11ed-be7d-3f8589292a29"
        b2b_contract_status, b2c_contract_status = "statusCreated", "statusCreated"

        b2c_contract = "contb2c_51e561c2-2ed2-11ed-be7d-3f8589292a29"

        obligation_state = "statePending"
        obligation_end_date = "2023-07-06"
        obligation_id = "ob_9e2bb1ce-2ed4-11ed-be7d-3f8589292a29"

        if b2c_contract != "" and b2b_contract != "" and consent_state != "empty":

            if consent_state in ['Invalid', 'Expired'] and b2b_contract_status \
                    not in ('statusViolated', 'statusTerminated', 'statusExpired'):
                r = requests.get(ContractApiTest.CONTRACT_URL +
                                 "/status/{}/{}/".format(b2b_contract, "statusExpired"))
                self.assertEqual(r.status_code, 200)

                r = requests.get(ContractApiTest.CONTRACT_URL +
                                 "/obligation/states/{}/{}/".format(obligation_id, "stateInvalid"))
                self.assertEqual(r.status_code, 200)

            else:
                if current_date > obligation_end_date and obligation_state == 'statePending' and b2b_contract_status not in (
                        'statusViolated', 'statusTerminated', 'statusExpired'):
                    print('b2b without consent')

                    r = requests.get(ContractApiTest.CONTRACT_URL +
                                     "/status/{}/{}/".format(b2b_contract, "statusViolated"))
                    self.assertEqual(r.status_code, 200)

                    r = requests.get(ContractApiTest.CONTRACT_URL +
                                     "/obligation/states/{}/{}/".format(obligation_id, "stateViolated"))
                    self.assertEqual(r.status_code, 200)


        elif b2c_contract != "" and consent_state != "empty":
            if consent_state in ['Invalid', 'Expired'] and b2c_contract_status \
                    not in ('statusViolated', 'statusTerminated', 'statusExpired'):
                r = requests.get(ContractApiTest.CONTRACT_URL +
                                 "/status/{}/{}/".format(b2b_contract, "statusExpired"))
                self.assertEqual(r.status_code, 200)

                r = requests.get(ContractApiTest.CONTRACT_URL +
                                 "/obligation/states/{}/{}/".format(obligation_id, "stateInvalid"))
                self.assertEqual(r.status_code, 200)
            else:
                if current_date > obligation_end_date and obligation_state == 'statePending' and b2b_contract_status not in (
                        'statusViolated', 'statusTerminated', 'statusExpired'):
                    r = requests.get(ContractApiTest.CONTRACT_URL +
                                     "/status/{}/{}/".format(b2c_contract, "statusViolated"))
                    self.assertEqual(r.status_code, 200)

                    r = requests.get(ContractApiTest.CONTRACT_URL +
                                     "/obligation/states/{}/{}/".format(obligation_id, "stateViolated"))
                    self.assertEqual(r.status_code, 200)

    def test_consent_expire_data_controller_still_use(self):
        current_date = "2023-09-06"

        b2b_contract = "contb2b_bfcff2dc-2ed3-11ed-be7d-3f8589292a29"
        b2b_contract_status, b2c_contract_status = "statusCreated", "statusCreated"

        # get obligation
        obligation_id = "ob_9e2bb1ce-2ed4-11ed-be7d-3f8589292a29"

        # get b2c contract reference
        contractIdB2C = "contb2c_51e561c2-2ed2-11ed-be7d-3f8589292a29"
        # get b2c
        b2c_contract = "contb2c_51e561c2-2ed2-11ed-be7d-3f8589292a29"
        consent_id = "cons_001"
        consent_state = "Invalid"

        if consent_state == "Invalid" and b2b_contract_status not in ['statusExpired', 'statusTerminated']:
            # get contractors
            r = requests.get(ContractApiTest.CONTRACT_URL +
                             "contractors/{}/".format(b2c_contract))
            self.assertEqual(r.status_code, 200)

            print("notify to the contractors")

    # complete contract compliance
    def test_contract_compliance_complete(self):
        r = requests.get(ContractApiTest.CONTRACT_URL + "compliance/")
        self.assertEqual(r.status_code, 200)

    # /******************************************************** end contract compliance ***************************/


if __name__ == "__main__":
    unittest.main()
