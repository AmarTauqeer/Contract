# Unit Test Results (i.e., unit test log) for CCV correctness verification
 
[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://travis-ci.org/joemccann/dillinger)


```sh
/home/amar/D/Projects/ReactDjango/ReactNextDjango/venv/bin/python /snap/pycharm-community/296/plugins/python-ce/helpers/pycharm/_jb_pytest_runner.py --path /home/amar/D/Projects/FlaskProject/Contract-shacl-repairs/backend/tests/contract_test.py 
Testing started at 10:55 ...
Launching pytest with arguments /home/amar/D/Projects/FlaskProject/Contract-shacl-repairs/backend/tests/contract_test.py --no-header --no-summary -q in /home/amar/D/Projects/FlaskProject/Contract-shacl-repairs/backend/tests

============================= test session starts ==============================
collecting ... collected 28 items

contract_test.py::ContractApiTest::test_b2b_b2c_with_consent 
contract_test.py::ContractApiTest::test_b2b_without_consent 
contract_test.py::ContractApiTest::test_b2c_without_consent 
contract_test.py::ContractApiTest::test_consent_expire_data_controller_still_use 
contract_test.py::ContractApiTest::test_contract_compliance_complete 
contract_test.py::ContractApiTest::test_get_all_contractors 
contract_test.py::ContractApiTest::test_get_all_contracts 
contract_test.py::ContractApiTest::test_get_all_obligations 
contract_test.py::ContractApiTest::test_get_all_signatures 
contract_test.py::ContractApiTest::test_get_all_term_types 
contract_test.py::ContractApiTest::test_get_contract_by_contractor 
contract_test.py::ContractApiTest::test_get_contract_by_id 
contract_test.py::ContractApiTest::test_get_contract_contractor 
contract_test.py::ContractApiTest::test_get_contractor_by_id 
contract_test.py::ContractApiTest::test_get_obligation_by_id 
contract_test.py::ContractApiTest::test_get_obligation_id 
contract_test.py::ContractApiTest::test_get_signatures_by_contractid 
contract_test.py::ContractApiTest::test_get_signatures_by_id 
contract_test.py::ContractApiTest::test_get_term_by_contract_id 
contract_test.py::ContractApiTest::test_get_term_type_by_id 
contract_test.py::ContractApiTest::test_new_contract 
contract_test.py::ContractApiTest::test_new_contract_term 
contract_test.py::ContractApiTest::test_new_contractor 
contract_test.py::ContractApiTest::test_new_term_type 
contract_test.py::ContractApiTest::test_update_contract 
contract_test.py::ContractApiTest::test_update_contract_term 
contract_test.py::ContractApiTest::test_update_contractor 
contract_test.py::ContractApiTest::test_update_term_type 

============================= 28 passed in 17.82s ==============================

Process finished with exit code 0
PASSED      [  3%]PASSED       [  7%]PASSED       [ 10%]b2c without consent
PASSED [ 14%]notify to the contractors
PASSED [ 17%]PASSED       [ 21%]PASSED         [ 25%]PASSED       [ 28%]PASSED        [ 32%]PASSED        [ 35%]PASSED [ 39%]PASSED        [ 42%]PASSED   [ 46%]PASSED      [ 50%]PASSED      [ 53%]PASSED         [ 57%]PASSED [ 60%]PASSED      [ 64%]PASSED   [ 67%]PASSED       [ 71%]PASSED              [ 75%]PASSED         [ 78%]PASSED            [ 82%]PASSED             [ 85%]PASSED           [ 89%]PASSED      [ 92%]PASSED         [ 96%]PASSED          [100%]
```


