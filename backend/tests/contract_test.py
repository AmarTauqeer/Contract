import unittest
import requests


class ContractApiTest(unittest.TestCase):
    # base url
    CONTRACT_URL = "http://172.25.5.173:5000/contract/"
    DATA = {
        "Amendment": "abccc",
        "ConfidentialityObligation": "string",
        "ContractId": "kgtest",
        "ContractProvider": "string",
        "ContractRequester": "string",
        "ContractType": "Written",
        "DataController": "string",
        "DataProtection": "Yes",
        "EffectiveDate": "2021-06-06",
        "ExecutionDate": "2021-06-06",
        "ExpireDate": "2022-06-06",
        "LimitationOnUse": "string",
        "Medium": "string",
        "MethodOfNotice": "string",
        "NoThirdPartyBeneficiaries": "string",
        "PermittedDisclosure": "string",
        "Purpose": "string",
        "ReceiptOfNotice": "string",
        "Severability": "string",
        "StartDate": "2021-06-06",
        "TerminationForInsolvency": "string",
        "TerminationForMaterialBreach": "string",
        "TerminationOnNotice": "string",
        "Waiver": "string",
        "ContractStatus": "Valid",
    }

    # get all contracts
    def test_get_all_contracts(self):
        r = requests.get(ContractApiTest.CONTRACT_URL + "list_of_contracts/")
        self.assertEqual(r.status_code, 200)


    # get all contracts
    def test_get_all_contractors(self):
        r = requests.get(ContractApiTest.CONTRACT_URL + "contractors/")
        self.assertEqual(r.status_code, 200)

    # get contract by requester
    def test_get_contract_by_requester(self):
        requester = 'CompanyABC'
        r = requests.get(ContractApiTest.CONTRACT_URL + "by_requester/{}/".format(requester))
        self.assertEqual(r.status_code, 200)

    # get contract by provider
    def test_get_contract_by_provider(self):
        provider = 'Brade'
        r = requests.get(ContractApiTest.CONTRACT_URL + "by_provider/{}/".format(provider))
        self.assertEqual(r.status_code, 200)

    # get contract by contract id
    def test_get_contract_by_id(self):
        id = 'kg244565'
        r = requests.get(ContractApiTest.CONTRACT_URL + "by_contractId/{}/".format(id))
        self.assertEqual(r.status_code, 200)

    # new contract
    def test_new_contract(self):
        r = requests.post(ContractApiTest.CONTRACT_URL + "create/", json=ContractApiTest.DATA)
        self.assertEqual(r.status_code, 200)

    # update contract
    def test_update_contract(self):
        r = requests.put(ContractApiTest.CONTRACT_URL + "update/", json=ContractApiTest.DATA)
        self.assertEqual(r.status_code, 200)

    # delete contract by contract id
    def test_get_contract_by_id(self):
        id = 'kgtest'
        r = requests.delete(ContractApiTest.CONTRACT_URL + "delete/{}/".format(id))
        self.assertEqual(r.status_code, 200)
