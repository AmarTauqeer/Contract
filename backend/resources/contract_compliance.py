from resources.contract_obligation import GetObligationIdentifierById, ObligationStatusUpdateById, \
    GetObligationByContractId
from resources.contracts import ContractByContractId, ContractStatusUpdateById, GetContractContractors
from resources.imports import *
from resources.schemas import *


class GetContractCompliance(MethodResource, Resource):
    @doc(description='Contract Compliance', tags=['Contract Compliance'])
    # @check_for_session
    # @Credentials.check_for_token
    # @marshal_with(BulkResponseQuerySchema)
    def get(self):
        query = QueryEngine()
        response = json.loads(
            query.select_query_gdb(purpose=None, dataRequester=None, additionalData="compliance", termID=None,
                                   contractRequester=None, contractProvider=None, ))

        obligatons = response["results"]['bindings']
        # current_data = date(2022, 4, 5)
        current_data = date.today()
        for x in obligatons:
            obligation_id = x["Obligation"]["value"][45:]
            sdate = x["exe_date"]["value"][45:]
            edate = x["end_date"]["value"][45:]
            obl_state = x["state"]["value"][45:]
            obl_desc = x["obl_desc"]["value"]

            ob = GetObligationIdentifierById.get(self, obligation_id)
            identifier_data = ob.json
            for i in identifier_data:
                if 'CONTB2B_' in i:
                    b2b_contract_status = ''
                    b2b_contract_id = ''
                    consent_state = 'Valid'
                    # get contract status
                    b2b_data = ContractByContractId.get(self, i)
                    b2b_data = b2b_data.json
                    b2b_contract_status = b2b_data["ContractStatus"]
                    b2b_contract_id = b2b_data["Contract"]
                    b2c_identifier = GetObligationIdentifierById.get(self, obligation_id)
                    b2c_identifier = b2c_identifier.json

                    date_time_str = edate
                    date_time_obj = datetime.strptime(date_time_str, '%Y-%m-%d').date()

                    for a in b2c_identifier:
                        if 'CONTB2C_' in a:
                            b2c_data = ContractByContractId.get(self, a)
                            b2c_data = b2c_data.json
                            b2c_contract_status = b2c_data["ContractStatus"]
                            b2c_contract_id = b2c_data["Contract"]

                            consent_id = b2c_data["ConsentId"]
                            consent_state = 'Valid'
                            # print(consent_state)
                            # consent based status

                            if consent_state in ['Invalid', 'Expired'] and b2c_contract_status \
                                    not in ('hasViolated', 'hasTerminated', 'hasExpired'):
                                print('if')
                                # update contract status
                                ContractStatusUpdateById.get(self, b2c_contract_id, 'hasExpired')
                                # update b2b contract status
                                ContractStatusUpdateById.get(self, b2b_contract_id, 'hasExpired')
                                # update b2b obligation
                                ObligationStatusUpdateById.get(self, obligation_id, 'hasExpired')
                                self.send_email('expire', b2b_contract_id, obl_desc, obligation_id)

                                b2c_obligation = GetObligationByContractId.get(self, b2c_contract_id)
                                b2c_obligation = b2c_obligation.json
                                for a in b2c_obligation:
                                    id = a['obligationID']
                                    description = a['description']
                                    print(id)
                                    ObligationStatusUpdateById.get(self, id, 'hasExpired')
                                    self.send_email('expire', b2c_contract_id, description, id)
                            else:
                                print('else')
                                b2c_obligation = GetObligationByContractId.get(self, b2c_contract_id)
                                b2c_obligation = b2c_obligation.json
                                for a in b2c_obligation:
                                    id = a['obligationID']
                                    state = a['state']
                                    description = a['description']
                                    # current_data=date(2023, 2, 11)
                                    if current_data >= date_time_obj and state == 'hasPendingState' \
                                            and b2c_contract_status not in (
                                    'hasViolated', 'hasTerminated', 'hasExpired'):
                                        ContractStatusUpdateById.get(self, b2c_contract_id, 'hasViolated')
                                        ObligationStatusUpdateById.get(self, id, 'hasViolated')
                                        self.send_email('violation', b2c_contract_id, description, id)

                    # b2b violation detection
                    print(consent_state)
                    if consent_state == 'Valid' and b2b_contract_id != '' and current_data >= date_time_obj \
                            and obl_state == 'hasPendingState' \
                            and b2b_contract_status not in ('hasViolated', 'hasTerminated'):
                        ContractStatusUpdateById.get(self, b2b_contract_id, 'hasViolated')
                        ObligationStatusUpdateById.get(self, obligation_id, 'hasViolated')
                        self.send_email('violation', b2b_contract_id, obl_desc, obligation_id)
        return 'Success'

    def send_email(self, type, contract_id, obl_desc, obligation_id):
        # Email to contractors in case of violation
        message_violation_expiration = ''
        if type == 'violation':
            message_violation_expiration = 'has been violated'
        else:
            message_violation_expiration = 'has been expired'

        message = 'In contract id = ' + str(
            contract_id) + ' ' + obl_desc + ' with obligation id ' + obligation_id + \
                  ' ' + message_violation_expiration
        from_email = 'act.contract.notification@gmail.com'
        # get contract contractors
        res = GetContractContractors.get(self, contract_id)
        contractors = res.json

        for c in contractors:
            email = c['email']
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(os.environ.get('MAIL_USERNAME'), os.environ.get('MAIL_PASSWORD'))
            server.sendmail(from_email, email, message)
