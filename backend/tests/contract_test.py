import unittest
import requests


class ContractApiTest(unittest.TestCase):
    # base url
    # CONTRACT_URL = "https://actool.contract.sti2.at/contract/"
    CONTRACT_URL = "http://172.25.3.6:5000/"
    term_type_data = {
        "Description": "new term",
        "Name": "new term name",
    }
    term_type_data_update = {
        "Description": "updated term",
        "Name": "updated term name",
        "TermTypeId": "Term_type_3f71a7b6-ea6d-11ec-8710-2f22ecd7a3cc"
    }

    term_data = {
        "ContractId": "CONTB2C_0ad9bf2c-c3a6-11ec-bb8b-1b75cc609c1a",
        "Description": "new term description",
        "TermTypeId": "Term_type_3f71a7b6-ea6d-11ec-8710-2f22ecd7a3cc",
    }
    term_data_update = {
        "ContractId": "CONTB2C_0ad9bf2c-c3a6-11ec-bb8b-1b75cc609c1a",
        "Description": "updated term description",
        "TermId": "Term_c3a113ee-ea6f-11ec-8710-2f22ecd7a3cc",
        "TermTypeId": "Term_type_3f71a7b6-ea6d-11ec-8710-2f22ecd7a3cc",
    }

    contractor_data = {
        "Name": "Amar Tauqeer",
        "Email": "amar.tauqeer@hotmail.com",
        "Phone": "004368864133065",
        "Address": "Techniker strasse 7/008 6020 Innsbruck Austria",
        "Country": "Austria",
        "Territory": "Innsbruck",
        "Role": "DataSubject",
    }

    contractor_data_update = {
        "ContractorId": "contractorid",
        "Name": "Amar Tauqeer",
        "Email": "amar.tauqeer@hotmail.com",
        "Phone": "004368864133065",
        "Address": "Techniker strasse 7/008 6020 Innsbruck Austria",
        "Country": "Austria",
        "Territory": "Innsbruck",
        "Role": "DataSubject",
    }

    contractor_signature_data = {
        "ContractId": "contractid",
        "ContractorId": "contractorid",
        "CreateDate": "2022-04-24",
        "Signature": "Amar tauqeer",
    }

    contractor_signature_data_update = {
        "SignatureId": "signatureid",
        "ContractId": "contractid",
        "ContractorId": "contractorid",
        "CreateDate": "2022-04-24",
        "Signature": "Amar tauqeer",
    }

    obligation_data = {
        "ContractId": "CONTB2C_0ad9bf2c-c3a6-11ec-bb8b-1b75cc609c1a",
        "ContractIdB2C": "",
        "ContractorId": "C_028da1e8-c3a7-11ec-bb8b-1b75cc609c1a",
        "Description": "obligation to deliver",
        "TermId": "Term_66b086a4-c3a7-11ec-bb8b-1b75cc609c1a",
        "ExecutionDate": "2022-04-24",
        "EndDate": "2023-04-24",
        "State": "hasPendingState",
    }

    contract_data = {
        "ConsentId": "CONS002",
        "ConsiderationDescription": "purpose of contract",
        "ConsiderationValue": "200",
        "ContractCategory": "hasBusinessToConsumer",
        "ContractStatus": "hasCreated",
        "ContractType": "Written",
        "Contractors": [
            "C_8bc15c10-b9b2-11ec-8fd7-efc66f58363f", "C_028da1e8-c3a7-11ec-bb8b-1b75cc609c1a"
        ],
        "EffectiveDate": "2022-04-24",
        "EndDate": "2023-04-24",
        "ExecutionDate": "2022-04-24",
        "Medium": "online",
        "Obligations": [

        ],
        "Purpose": "selling data",
        "Signatures": [

        ],
        "Terms": [

        ],
    }

    contract_update_data = {
        "ConsentId": "CONS002",
        "ConsiderationDescription": "purpose of contract",
        "ConsiderationValue": "200",
        "ContractCategory": "hasBusinessToConsumer",
        "ContractId": "CONTB2C_0ad9bf2c-c3a6-11ec-bb8b-1b75cc609c1a",
        "ContractStatus": "hasUpdated",
        "ContractType": "Written",
        "Contractors": [
            "C_8bc15c10-b9b2-11ec-8fd7-efc66f58363f", "C_028da1e8-c3a7-11ec-bb8b-1b75cc609c1a"
        ],
        "EffectiveDate": "2022-04-24",
        "EndDate": "2023-04-24",
        "ExecutionDate": "2022-04-24",
        "Medium": "online",
        "Obligations": [
            "OB_b667bff0-c3a7-11ec-bb8b-1b75cc609c1a"
        ],
        "Purpose": "selling data",
        "Signatures": [
            "Sig_debaa4f4-c3a7-11ec-bb8b-1b75cc609c1a",
            "Sig_d059468c-c3ab-11ec-bb8b-1b75cc609c1a"
        ],
        "Terms": [
            "Term_66b086a4-c3a7-11ec-bb8b-1b75cc609c1a", "Term_c3a113ee-ea6f-11ec-8710-2f22ecd7a3cc"
        ],
    }

    # /******************************************************** contracts ***************************/
    # get all contracts
    def test_get_all_contracts(self):
        r = requests.get(ContractApiTest.CONTRACT_URL + "contract/list_of_contracts/")
        self.assertEqual(r.status_code, 200)

    # get contract by contractor
    def test_get_contract_by_contractor(self):
        contractor = 'C_8bc15c10-b9b2-11ec-8fd7-efc66f58363f'
        r = requests.get(ContractApiTest.CONTRACT_URL +
                         "contract/byContractor/{}".format(contractor))
        self.assertEqual(r.status_code, 200)

    # get contract by contract id
    def test_get_contract_by_id(self):
        contractid = 'CONTB2C_0ad9bf2c-c3a6-11ec-bb8b-1b75cc609c1a'
        r = requests.get(ContractApiTest.CONTRACT_URL +
                         "contract/byContract/{}".format(contractid))
        self.assertEqual(r.status_code, 200)

    # new contract
    def test_new_contract(self):
        r = requests.post(ContractApiTest.CONTRACT_URL +
                          "contract/create/", json=ContractApiTest.contract_data)
        self.assertEqual(r.status_code, 200)

    # update contract
    def test_update_contract(self):
        r = requests.put(ContractApiTest.CONTRACT_URL +
                         "contract/update/", json=ContractApiTest.contract_update_data)
        self.assertEqual(r.status_code, 200)

    # /******************************************************** end contracts ***************************/

    # /******************************************************** contractors ***************************/
    # get all contractors
    def test_get_all_contractors(self):
        r = requests.get(ContractApiTest.CONTRACT_URL + "contractors/")
        self.assertEqual(r.status_code, 200)

    # get contractor by id
    def test_get_contractor_by_id(self):
        contractorid = 'C_8bc15c10-b9b2-11ec-8fd7-efc66f58363f'
        r = requests.get(ContractApiTest.CONTRACT_URL +
                         "contractor/{}".format(contractorid))
        self.assertEqual(r.status_code, 200)

    # get contract contractor
    def test_get_contract_contractor(self):
        contractid = 'CONTB2C_0ad9bf2c-c3a6-11ec-bb8b-1b75cc609c1a'
        r = requests.get(ContractApiTest.CONTRACT_URL +
                         "contract/contractors/{}".format(contractid))
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
        term_type_id = 'Term_type_f2b747f6-b9b0-11ec-8fd7-efc66f58363f'
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

    # delete term type by id
    def test_delete_term_type_by_id(self):
        id = 'Term_type_4b28399a-eb0c-11ec-b0a1-a708bb8575ed'
        r = requests.delete(ContractApiTest.CONTRACT_URL +
                            "term/type/delete/{}/".format(id))
        self.assertEqual(r.status_code, 200)

    # /******************************************************** end term types ***************************/

    # /******************************************************** contract term ***************************/
    # get term by contract id
    def test_get_term_by_contract_id(self):
        contract_id = 'Term_66b086a4-c3a7-11ec-bb8b-1b75cc609c1a'
        r = requests.get(ContractApiTest.CONTRACT_URL +
                         "contract/term/{}".format(contract_id))
        self.assertEqual(r.status_code, 200)

    # new contract term
    def test_new_contract_term(self):
        r = requests.post(ContractApiTest.CONTRACT_URL +
                          "contract/term/create/", json=ContractApiTest.term_data)
        self.assertEqual(r.status_code, 200)

    # update contract term
    def test_update_contract_term(self):
        r = requests.put(ContractApiTest.CONTRACT_URL +
                         "contract/term/update/", json=ContractApiTest.term_data_update)
        self.assertEqual(r.status_code, 200)

    # delete contract term by contract id
    def test_delete_contract_term_by_id(self):
        id = 'Term_66b086a4-c3a7-11ec-bb8b-1b75cc609c1a'
        r = requests.delete(ContractApiTest.CONTRACT_URL +
                            "contract/term/delete/{}/".format(id))
        self.assertEqual(r.status_code, 200)

    # /******************************************************** end contract term ***************************/

    # /******************************************************** contract obligation ***************************/
    # get all obligations
    def test_get_all_obligations(self):
        r = requests.get(ContractApiTest.CONTRACT_URL + "obligations/")
        self.assertEqual(r.status_code, 200)

    # get obligation by id
    def test_get_obligation_id(self):
        obligation_id = 'OB_b667bff0-c3a7-11ec-bb8b-1b75cc609c1a'
        r = requests.get(ContractApiTest.CONTRACT_URL +
                         "obligation/{}".format(obligation_id))
        self.assertEqual(r.status_code, 200)

    # get obligation by id
    def test_get_obligation_by_id(self):
        obligation_id = 'OB_b667bff0-c3a7-11ec-bb8b-1b75cc609c1a'
        r = requests.get(ContractApiTest.CONTRACT_URL +
                         "obligation/{}".format(obligation_id))
        self.assertEqual(r.status_code, 200)

    # # new contract obligation
    # def test_new_contract_obligation(self):
    #     r = requests.post(ContractApiTest.CONTRACT_URL +
    #                       "obligation/create/", json=ContractApiTest.obligation_data)
    #     self.assertEqual(r.status_code, 200)

    # delete obligation by id
    def test_delete_obligation_by_id(self):
        id = 'OB_b667bff0-c3a7-11ec-bb8b-1b75cc609c1a'
        r = requests.delete(ContractApiTest.CONTRACT_URL +
                            "obligation/delete/{}/".format(id))
        self.assertEqual(r.status_code, 200)

    # /******************************************************** end contract obligation ***************************/

    # /******************************************************** contract signature ***************************/
    # get all signatures
    def test_get_all_signatures(self):
        r = requests.get(ContractApiTest.CONTRACT_URL + "signatures/")
        self.assertEqual(r.status_code, 200)

    # get signatures by contractid
    def test_get_signatures_by_contractid(self):
        contractid = 'CONTB2C_0ad9bf2c-c3a6-11ec-bb8b-1b75cc609c1a'
        r = requests.get(ContractApiTest.CONTRACT_URL +
                         "contract/signatures/{}".format(contractid))
        self.assertEqual(r.status_code, 200)

    # get signatures by id
    def test_get_signatures_by_id(self):
        signatureid = 'Sig_d059468c-c3ab-11ec-bb8b-1b75cc609c1a'
        r = requests.get(ContractApiTest.CONTRACT_URL +
                         "/signature/{}".format(signatureid))
        self.assertEqual(r.status_code, 200)

    # /******************************************************** end contract signature ***************************/

    # /******************************************************** contract compliance ***************************/

    # # contract compliance
    # def test_contract_compliance(self):
    #     r = requests.get(ContractApiTest.CONTRACT_URL + "contract/compliance/")
    #     self.assertEqual(r.status_code, 200)

    # /******************************************************** end contract compliance ***************************/

    # # delete contract by contract id
    # def test_get_contract_by_id(self):
    #     id = 'kgtest'
    #     r = requests.delete(ContractApiTest.CONTRACT_URL +
    #                         "delete/{}/".format(id))
    #     self.assertEqual(r.status_code, 200)


if __name__ == "__main__":
    unittest.main()
