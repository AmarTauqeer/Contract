from core.security.RsaAesDecryption import RsaAesDecrypt
from resources.contract_obligation import GetObligationByContractId, ObligationDeleteById
from resources.contract_signatures import GetContractSignatures, SignatureDeleteById
from resources.contract_terms import GetContractTerms, TermDeleteById
from resources.imports import *
from resources.schemas import *


class Contracts(MethodResource, Resource):
    @doc(description='Contracts', tags=['Contracts'])
    # @check_for_session
    # @Credentials.check_for_token
    # @marshal_with(BulkResponseQuerySchema)
    def get(self):
        query = QueryEngine()
        response = json.loads(
            query.select_query_gdb(purpose=None, dataRequester=None, additionalData="bcontractId", contractID=None,
                                   contractRequester=None, contractProvider=None))

        if len(response["results"]['bindings']) != 0:
            data = response["results"]['bindings']
            all_data = []
            for d in data:
                contractor_array = []
                term_array = []
                obligation_array = []
                signature_array = []

                contid = d['contractId']['value']
                # print(contid)

                # get contractors
                contractors = GetContractContractors.get(self, contid)
                contractors = contractors.json
                if contractors != 'No record found for this ID':
                    for c in contractors:
                        cid = c['contractorId']
                        contractor_array.append(cid)

                # get terms
                terms = GetContractTerms.get(self, contid)
                terms = terms.json
                if terms != 'No record found for this ID':
                    for t in terms:
                        tid = t['termId']
                        term_array.append(tid)

                # get obligation
                obl = GetObligationByContractId.get(self, contid)
                obl = obl.json
                if obl != 'No record found for this ID':
                    for o in obl:
                        oid = o['obligationId']
                        obligation_array.append(oid)

                # get signatures
                sig = GetContractSignatures.get(self, contid)
                sig = sig.json
                if sig != 'No record found for this ID':
                    for s in sig:
                        sid = s['signatureId']
                        signature_array.append(sid)

                obj = {
                    'contractors': contractor_array,
                    'terms': term_array,
                    'obligations': obligation_array,
                    'signatures': signature_array
                }

                consentId = d['consentId']['value']

                category_data = d['contractCategory']['value'][45:]
                if category_data != 'categoryBusinessToConsumer':
                    category_data = 'categoryBusinessToBusiness'
                    consentId = ''
                new_data = {
                    'contractId': d['contractId']['value'],
                    'contractStatus': d['contractStatus']['value'][45:],
                    'contractCategory': category_data,
                    'consentId': consentId,
                    'purpose': d['purpose']['value'],
                    'contractType': d['contractType']['value'][45:],
                    'effectiveDate': d['effectiveDate']['value'],
                    'executionDate': d['executionDate']['value'],
                    'endDate': d['endDate']['value'],
                    'medium': d['medium']['value'],
                    'consideration': d['consideration']['value'],
                    'value': d['value']['value'],
                    'identifiers': obj
                }

                all_data.append(new_data)
            if len(all_data) != 0:
                return all_data
        return 'No record is found'


class ContractByContractor(MethodResource, Resource):
    @doc(description='Contracts', tags=['Contracts'])
    # @check_for_session
    # @Credentials.check_for_token
    # @marshal_with(BulkResponseQuerySchema)
    def get(self, contractorID):
        query = QueryEngine()
        response = json.loads(
            query.select_query_gdb(purpose=None, dataRequester=None, additionalData="contractByContractorID",
                                   contractorID=contractorID,
                                   contractRequester=None, contractProvider=None))
        response = response["results"]['bindings']
        if len(response) != 0:
            main_data = []
            for r in response:
                contract_id = r['Contract']['value'][45:]
                res = ContractByContractId.get(self, contract_id)
                # print(res.json)
                if res != 'No record found for this ID':
                    data = res.json
                    main_data.append(data)
            return main_data
        return 'No record found for this ID'


class ContractByProvider(MethodResource, Resource):
    # @check_for_session
    # @Credentials.check_for_token
    # @marshal_with(BulkResponseQuerySchema)
    def get(self, provider):
        query = QueryEngine()
        response = json.loads(
            query.select_query_gdb(purpose=None, dataRequester=None, additionalData="contractID", contractID=None,
                                   contractRequester=None, contractProvider=provider))
        response = response["results"]
        return response, 200


class ContractByContractId(MethodResource, Resource):
    @doc(description='Contracts', tags=['Contracts'])
    # @check_for_session
    # @Credentials.check_for_token
    # @marshal_with(BulkResponseQuerySchema)
    def get(self, contractID):
        query = QueryEngine()
        response = json.loads(
            query.select_query_gdb(purpose=None, dataRequester=None, additionalData="contractID", contractID=contractID,
                                   contractRequester=None, contractProvider=None, contractorID=None))

        data = response["results"]['bindings']
        if len(data) != 0:
            contractor_array = []
            term_array = []
            obligation_array = []
            signature_array = []

            for d in data:

                # get contractors
                contractors = GetContractContractors.get(self, contractID)
                contractors = contractors.json
                if contractors != 'No record found for this ID':
                    for c in contractors:
                        cid = c['contractorId']
                        contractor_array.append(cid)

                # get terms
                terms = GetContractTerms.get(self, contractID)
                terms = terms.json
                if terms != 'No record found for this ID':
                    for t in terms:
                        tid = t['termId']
                        term_array.append(tid)

                # get obligation
                obl = GetObligationByContractId.get(self, contractID)
                obl = obl.json

                if obl != 'No record found for this ID':
                    for o in obl:
                        oid = o['obligationId']
                        obligation_array.append(oid)

                # get signatures
                sig = GetContractSignatures.get(self, contractID)
                sig = sig.json
                # print(sig)
                if sig != 'No record found for this ID':
                    for s in sig:
                        # print(s)
                        sid = s['signatureId']
                        signature_array.append(sid)

            obj = {
                'contractors': contractor_array,
                'terms': term_array,
                'obligations': obligation_array,
                'signatures': signature_array
            }

            consentId = d['consentId']['value']

            category_data = d['contractCategory']['value'][45:]
            if category_data != 'categoryBusinessToConsumer':
                category_data = 'categoryBusinessToBusiness'
                consentId = ''
            new_data = {
                'contractId': d['contractId']['value'],
                'contractStatus': d['contractStatus']['value'][45:],
                'contractCategory': category_data,
                'consentId': consentId,
                'purpose': d['purpose']['value'],
                'contractType': d['contractType']['value'][45:],
                'effectiveDate': d['effectiveDate']['value'],
                'executionDate': d['executionDate']['value'],
                'endDate': d['endDate']['value'],
                'medium': d['medium']['value'],
                'consideration': d['consideration']['value'],
                'value': d['value']['value'],
                'identifiers': obj
            }
            data = new_data
            if len(data) != 0:
                return data
        return 'No data found for this ID'


class ContractUpdate(MethodResource, Resource):
    @doc(description='Contracts', tags=['Contracts'])
    # @check_for_session
    # @Credentials.check_for_token
    @marshal_with(BulkResponseQuerySchema)
    @use_kwargs(ContractUpdateSchema)
    def put(self, **kwargs):
        schema_serializer = ContractUpdateSchema()
        data = request.get_json(force=True)
        contract_id = data['ContractId']
        # get contract status from db
        result = ContractByContractId.get(self, contract_id)
        my_json = result.data.decode('utf8')
        decoded_data = json.loads(my_json)
        # print(decoded_data)
        if decoded_data != 'No data found for this ID':
            if decoded_data['contractId'] == contract_id:
                status_value = decoded_data['contractStatus']
                signed = re.findall(r"Signed", status_value)
                if len(signed) == 0:
                    validated_data = schema_serializer.load(data)
                    cv = ContractValidation()
                    response = cv.post_data(validated_data, type="update", contract_id=None)
                    if (response):
                        return jsonify({'Success': "Record updated successfully"})
                    else:
                        return jsonify({'Error': "Record not updated due to some errors."})
                else:
                    return jsonify({'Error': "Contract can't be modified after signed"})
            return jsonify({'Error': "Contract doesn't match with this ID"})
        return jsonify({'Success': "No record found for this ID"})


class ContractCreate(MethodResource, Resource):
    @doc(description='Contracts', tags=['Contracts'])
    # @check_for_session
    # @Credentials.check_for_token
    @use_kwargs(ContractRequestSchema)
    def post(self, **kwargs):
        schema_serializer = ContractRequestSchema()
        data = request.get_json(force=True)
        contract_category = data["ContractCategory"]
        uuidOne = uuid.uuid1()
        if contract_category == 'categoryBusinessToBusiness':
            contract_id = "contb2b_" + str(uuidOne)
        else:
            contract_id = "contb2c_" + str(uuidOne)
        validated_data = schema_serializer.load(data)
        cv = ContractValidation()
        response = cv.post_data(validated_data, type="insert", contract_id=contract_id)
        if response == 'Success':
            contract_obj = ContractByContractId.get(self, contract_id)
            # print(contract_obj.json)
            contract_obj = contract_obj.json
            return contract_obj
        else:
            return jsonify({'Error': "Record not inserted due to some errors."})


class ContractDeleteById(MethodResource, Resource):
    @doc(description='Contracts', tags=['Contracts'])
    # @check_for_session
    # @Credentials.check_for_token
    # @marshal_with(BulkResponseQuerySchema)
    # @use_kwargs(ContractRequestSchema)
    def delete(self, contractID):
        # get contract status from db
        result = ContractByContractId.get(self, contractID)
        my_json = result.data.decode('utf8')
        decoded_data = json.loads(my_json)
        # print(decoded_data)
        if decoded_data != 'No data found for this ID' and decoded_data['contractId'] == contractID:
            status_value = decoded_data['contractStatus']
            signed = re.findall(r"Signed", status_value)
            if len(signed) == 0:
                # delete obligation
                obl = GetObligationByContractId.get(self, contractID)
                my_json = obl.data.decode('utf-8')
                decoded_data = json.loads(my_json)
                if decoded_data != 'No record found for this ID':
                    obl_data = decoded_data
                    for o in obl_data:
                        obligation_id = o['obligationId'];
                        ObligationDeleteById.delete(self, obligation_id)

                # delete term
                obl = GetContractTerms.get(self, contractID)
                my_json = obl.data.decode('utf-8')
                decoded_data = json.loads(my_json)
                if decoded_data != 'No record found for this ID':
                    term_data = decoded_data
                    for t in term_data:
                        term_id = t['termId'];
                        TermDeleteById.delete(self, term_id)

                # delete signature
                obl = GetContractSignatures.get(self, contractID)
                my_json = obl.data.decode('utf-8')
                decoded_data = json.loads(my_json)
                if decoded_data != 'No record found for this ID':
                    sig_data = decoded_data
                    for s in sig_data:
                        sig_id = s['signatureId'];
                        SignatureDeleteById.delete(self, sig_id)

                cv = ContractValidation()

                response = cv.delete_contract(contractID)

                if (response):
                    return jsonify({'Success': "Record deleted successfully."})
                else:
                    return jsonify({'Error': "Record not deleted due to some errors."})
            else:
                return jsonify({'Error': "Contract can't be deleted after signed"})
        else:
            return jsonify({'Error': "Contract doesn't exist for this ID"})


class GetContractContractors(MethodResource, Resource):
    @doc(description='Contract Contractors', tags=['Contract Contractors'])
    # @check_for_session
    # @Credentials.check_for_token
    # @marshal_with(BulkResponseQuerySchema)
    def get(self, contractID):
        query = QueryEngine()
        response = json.loads(
            query.select_query_gdb(purpose=None, dataRequester=None, additionalData="contractContractors",
                                   contractID=contractID,
                                   contractRequester=None, contractProvider=None, contractorID=None, termID=None
                                   ))
        data = response["results"]["bindings"]
        if len(data) != 0:
            contractor_array = []
            for d in data:
                contractorId = d['contractorId']['value']
                obj_dec = RsaAesDecrypt()
                data = {'contractor_id': d['contractorId']['value'], 'name': d['name']['value'],
                        'email': d['email']['value'],
                        'phone': d['phone']['value'],
                        'address': d['address']['value'],
                        'country': d['country']['value'],
                        'vat': d['vat']['value'],
                        'territory': d['territory']['value']}
                decrypted_result = obj_dec.rsa_aes_decrypt(data)
                name = decrypted_result[0]['name']
                email = decrypted_result[1]['email']
                phone = decrypted_result[2]['phone']
                address = decrypted_result[3]['address']
                country = decrypted_result[4]['country']
                vat = decrypted_result[5]['vat']
                territory = decrypted_result[6]['territory']

                new_data = {'contractorId': contractorId,
                            'name': name,  # d['name']['value'],
                            'email': email,  # d['email']['value'],
                            'phone': phone,  # d['email']['value'],
                            'address': address,  # d['email']['value'],
                            'country': country,  # d['country']['value'],
                            'territory': territory,  # d['territory']['value'],
                            'vat': vat,  # d['email']['value'],
                            'createDate': d['createDate']['value']
                            }
                contractor_array.append(new_data)
            return contractor_array
        return 'No record found for this ID'


class ContractStatusUpdateById(MethodResource, Resource):
    @doc(description='Contracts', tags=['Contracts'])
    # @Credentials.check_for_token
    def get(self, contractID, status):

        host_post = os.getenv("HOST_URI_POST")
        hostname = host_post
        userid = os.getenv("user_name")
        password = os.getenv("password")

        violation_date = datetime.now()
        sparql = SPARQLWrapper(hostname)
        sparql.setHTTPAuth(BASIC)
        sparql.setCredentials(userid, password)
        query = textwrap.dedent("""
         PREFIX : <http://ontologies.atb-bremen.de/smashHitCore#>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX dc: <http://purl.org/dc/elements/1.1/>
            PREFIX dpv: <http://www.w3.org/ns/dpv#>
            PREFIX prov: <http://www.w3.org/ns/prov#>
            PREFIX dcat: <http://www.w3.org/ns/dcat#>
            PREFIX fibo-fnd-agr-ctr: <https://spec.edmcouncil.org/fibo/ontology/FND/Agreements/Contracts/>
            PREFIX dct: <http://purl.org/dc/terms/>
            DELETE {{?Contract :hasContractStatus :statusCreated.
                    ?Contract :hasContractStatus :statusRenewed.
                    ?Contract :hasContractStatus :statusPending.
                    ?Contract :hasContractStatus :statusViolated.
                    ?Contract :hasContractStatus :statusExpired.
                    ?Contract :hasContractStatus :statusSigned.
                    ?Contract :hasContractStatus :statusUpdated.
                    ?Contract :hasContractStatus :statusTerminated.}}
            INSERT {{?Contract :hasContractStatus :{2}.
            ?contractId :RevokedAtTime {0}.
            }}
             WHERE {{
             ?Contract rdf:type fibo-fnd-agr-ctr:Contract;
                        :contractID ?contractId;
              FILTER(?contractId = "{1}")
             }}""").format('\'{}^^xsd:dateTime\''.format(violation_date), contractID, status)

        # print(query)
        sparql.setQuery(query)
        sparql.method = "POST"
        sparql.queryType = "INSERT"
        sparql.setReturnFormat('json')
        result = sparql.query()
        if str(result.response.read().decode("utf-8")) == "":
            return "Success"
        else:
            return "Fail"

# class GetContractTestResult(MethodResource, Resource):
#     # @Credentials.check_for_token
#     # @marshal_with(BulkResponseQuerySchema)
#     def get(self):
#         response=ContractApiTest.test_get_all_contracts()
#         return response, 200
