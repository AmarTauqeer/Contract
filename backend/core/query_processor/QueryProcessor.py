from core.Credentials import Credentials
from core.storage.Sparql import SPARQL
from helper.Helper import HelperContract
import textwrap
from datetime import date


class QueryEngine (Credentials, SPARQL, HelperContract):
    def __init__(self):
        super().__init__()

    def prefix(self):
        prefix = textwrap.dedent("""PREFIX : <http://ontologies.atb-bremen.de/smashHitCore#>
            PREFIX gconsent: <https://w3id.org/GConsent#>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX dc: <http://purl.org/dc/elements/1.1/>
            PREFIX dpv: <http://www.w3.org/ns/dpv#>
            PREFIX prov: <http://www.w3.org/ns/prov#>
            PREFIX dcat: <http://www.w3.org/ns/dcat#>
            PREFIX fibo-fnd-agr-ctr: <https://spec.edmcouncil.org/fibo/ontology/FND/Agreements/Contracts/>
            PREFIX dct: <http://purl.org/dc/terms/>
        """)
        return prefix

    def get_all_contracts(self):
        query = textwrap.dedent("""{0}
            select * 
            where{{  ?Contract a :ContractId;
                        :hasContractStatus ?ContractStatus;
                        :forPurpose ?Purpose;
                        :contractType ?ContractType;
                        :hasDataController ?DataController;
                        :ContractRequester ?ContractRequester;
                        :ContractProvider ?ContractProvider;
                        dcat:startDate ?StartDate;
                        dcat:endDate ?EndingDate;
                        fibo-fnd-agr-ctr:hasEffectiveDate ?EffectiveDate;
                        fibo-fnd-agr-ctr:hasExecutionDate ?ExecutionDate;
                        :inMedium ?Medium;
                        :hasWaiver ?Waiver;
                        :hasAmendment ?Amendment;
                        :hasConfidentialityObligation ?ConfidentialityObligation;
                        :hasDataProtection ?DataProtection;
                        :hasLimitationOnUse ?LimitationOnUse;
                        :hasMethodOfNotice ?MethodOfNotice;
                        :hasNoThirdPartyBeneficiaries ?NoThirdPartyBeneficiaries;
                        :hasPermittedDisclosure ?PermittedDisclosure;
                        :hasReceiptOfNotice ?ReceiptOfNotice;
                        :hasSeverability ?Severability;
                        :hasTerminationForInsolvency ?TerminationForInsolvency;
                        :hasTerminationForMaterialBreach ?TerminationForMaterialBreach;
                        :hasTerminationOnNotice ?TerminationOnNotice .
        }}
        """).format(self.prefix())
        return query

    def get_contract_by_requester(self, name):
        query = textwrap.dedent("""{0}
                SELECT ?Contract   
                    WHERE {{ 
                    ?Contract a :ContractId;
                            :ContractRequester :{1}.
                }}""").format(self.prefix(), name)
        return query

    def get_contract_by_provider(self, name):
        query = textwrap.dedent("""{0}
            SELECT ?Contract   
                WHERE {{ 
                ?Contract a :ContractId;
                        :ContractProvider :{1}.
            }}""").format(self.prefix(), name)
        return query

    def get_contract_by_id(self, id):
        query = textwrap.dedent("""{0}
            SELECT *   
                WHERE {{ 
                ?Contract a :ContractId;
                filter(?Contract=:{1}) .
            }}""").format(self.prefix(), id)
        return query

    def insert_query(self, ContractId, ContractType, Purpose,
                     ContractRequester, ContractProvider, DataController, StartDate,
                     ExecutionDate, EffectiveDate, ExpireDate, Medium, Waiver, Amendment,
                     ConfidentialityObligation, DataProtection, LimitationOnUse,
                     MethodOfNotice, NoThirdPartyBeneficiaries, PermittedDisclosure,
                     ReceiptOfNotice, Severability, TerminationForInsolvency,
                     TerminationForMaterialBreach, TerminationOnNotice, ContractStatus):
        insquery = textwrap.dedent("""{0} 
            INSERT DATA {{
            :{1} a <http://ontologies.atb-bremen.de/smashHitCore#ContractId>;
            :contractType :{2};
                       :forPurpose "{3}";
                       :ContractRequester :{4};
                       :ContractProvider :{5};
                       :hasDataController :{6};
                        dcat:startDate :{7};
                        fibo-fnd-agr-ctr:hasExecutionDate :{8};
                        fibo-fnd-agr-ctr:hasEffectiveDate :{9};
                        dcat:endDate :{10};
                        :inMedium "{11}";
                        :hasWaiver "{12}";
                        :hasAmendment "{13}";
                        :hasConfidentialityObligation "{14}";
                        :hasDataProtection "{15}";
                        :hasLimitationOnUse "{16}";
                        :hasMethodOfNotice "{17}";
                        :hasNoThirdPartyBeneficiaries "{18}";
                        :hasPermittedDisclosure "{19}";
                        :hasReceiptOfNotice "{20}";
                        :hasSeverability "{21}";
                        :hasTerminationForInsolvency "{22}";
                        :hasTerminationForMaterialBreach "{23}";
                        :hasTerminationOnNotice "{24}";
                        :hasContractStatus :{25} .
                   }}       
               
          """.format(self.prefix(), ContractId, ContractType,
                     Purpose, ContractRequester,
                     ContractProvider, DataController, StartDate,
                     ExecutionDate, EffectiveDate, ExpireDate, Medium, Waiver, Amendment,
                     ConfidentialityObligation, DataProtection, LimitationOnUse,
                     MethodOfNotice, NoThirdPartyBeneficiaries, PermittedDisclosure,
                     ReceiptOfNotice, Severability, TerminationForInsolvency,
                     TerminationForMaterialBreach, TerminationOnNotice, ContractStatus))
        return insquery
