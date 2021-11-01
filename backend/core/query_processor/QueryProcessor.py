from core.Credentials import Credentials
from core.storage.Sparql import SPARQL
from helper.Helper import HelperContract
import textwrap
from datetime import date


class QueryEngine(Credentials, SPARQL, HelperContract):
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
            where{{  ?Contract a :contractID;
                        :hasContractStatus ?ContractStatus;
                        :forPurpose ?Purpose;
                        :contractType ?ContractType;
                        :DataController ?DataController;
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
                    ?Contract a :contractID;
                            :ContractRequester :{1}.
                }}""").format(self.prefix(), name)
        return query

    def get_contract_by_provider(self, name):
        query = textwrap.dedent("""{0}
            SELECT ?Contract   
                WHERE {{ 
                ?Contract a :contractID;
                        :ContractProvider :{1}.
            }}""").format(self.prefix(), name)
        return query

    def get_contract_by_id(self, id):
        query = textwrap.dedent("""{0}
            SELECT *   
                WHERE {{ 
                ?Contract a :contractID;
                        :hasContractStatus ?ContractStatus;
                        :forPurpose ?Purpose;
                        :contractType ?ContractType;
                        :DataController ?DataController;
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
                filter(?Contract=:{1}) .
            }}""").format(self.prefix(), id)

        return query

    def get_agent_by_id(self, id):
        query = textwrap.dedent("""{0}
            SELECT *   
                WHERE {{ 
                ?Agent a :agentID;
                        :hasType ?type;
                        :hasName ?name;
                        :hasEmail ?email;
                        :hasAddress ?address;
                optional{{?Agent :hasTelephone ?phone.}}                        
                optional{{?Agent :atCity ?city.}}
                optional{{?Agent :atState ?state.}}
                optional{{?Agent :atCountry ?country.}}
                filter(?Agent=:{1}) .
            }}""").format(self.prefix(), id)

        return query

    def delete_contract_by_id(self, id):
        query = textwrap.dedent("""{0}
                delete{{?s ?p ?o}}   
                    WHERE {{ 
                    select ?s ?p ?o
                        where{{
                            ?s ?p ?o .
                            filter(?s=:{1})
                }}}}""").format(self.prefix(), id)
        # print(query)
        return query

    def delete_agent_by_id(self, id):
        query = textwrap.dedent("""{0}
                delete{{?s ?p ?o}}   
                    WHERE {{ 
                    select ?s ?p ?o
                        where{{
                            ?s ?p ?o .
                            filter(?s=:{1})
                }}}}""").format(self.prefix(), id)
        # print(query)
        return query

    def get_all_agents(self):
        query = textwrap.dedent("""{0}
            select *
            where{{  ?Agent a :agentID;
                        :hasName ?Name;
                        :hasAddress ?Address .
             		optional{{?Agent :hasEmail ?email.}}
    				optional{{?Agent :hasTelephone ?telephone .}}
    				optional{{?Agent :atCity ?city.}}
    				optional{{?Agent :atState ?state.}}
    				optional{{?Agent :atCountry ?country.}}
        }}
        """).format(self.prefix())
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
            :{1} a <http://ontologies.atb-bremen.de/smashHitCore#contractID>;
            :contractType :{2};
                       :forPurpose "{3}";
                       :ContractRequester :{4};
                       :ContractProvider :{5};
                       :DataController :{6};
                        dcat:startDate "{7}";
                        fibo-fnd-agr-ctr:hasExecutionDate "{8}";
                        fibo-fnd-agr-ctr:hasEffectiveDate "{9}";
                        dcat:endDate "{10}";
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

    def insert_query_agent(self, AgentId, AgentType, Name, Email, Phone, Address, City, State, Country):
        insquery = textwrap.dedent("""{0} 
        INSERT DATA {{
            :{1} a <http://ontologies.atb-bremen.de/smashHitCore#agentID>;
            :hasType "{2}";
                        :hasName "{3}";
                        :hasEmail "{4}";
                        :hasTelephone "{5}";
                        :hasAddress "{6}";
                        :atCity "{7}";
                        :atState "{8}";
                        :atCountry "{9}" .
                   }}       
          """.format(self.prefix(), AgentId, AgentType, Name, Email, Phone, Address, City, State, Country))
        return insquery
