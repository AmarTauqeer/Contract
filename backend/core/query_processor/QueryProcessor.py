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
    	    :hasContractCategory ?ContractCategory;
		    :forPurpose ?Purpose;
		    :contractType ?ContractType;
		    fibo-fnd-agr-ctr:hasEffectiveDate ?EffectiveDate;
		    fibo-fnd-agr-ctr:hasExecutionDate ?ExecutionDate;
		    :hasEndDate ?EndDate;
            :inMedium ?Medium;
            dct:description ?consideration;
            rdf:value ?value .
        }}
        """).format(self.prefix())
        return query

    def get_contract_by_contractor(self, name):
        query = textwrap.dedent("""{0}
                SELECT ?Contract   
                    WHERE {{ 
                     ?Contract a :contractID;
                        :hasContractors ?contractors .
                    filter(?contractors=:{1})
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
    	        :hasContractCategory ?ContractCategory;
		        :forPurpose ?Purpose;
		        :contractType ?ContractType;
		        fibo-fnd-agr-ctr:hasEffectiveDate ?EffectiveDate;
		        fibo-fnd-agr-ctr:hasExecutionDate ?ExecutionDate;
		        :hasEndDate ?EndDate;
                :inMedium ?Medium;
                dct:description ?consideration;
                rdf:value ?value .
                
                filter(?Contract=:{1}) .
            }}""").format(self.prefix(), id)

        return query

    def get_contractor_by_id(self, id):
        query = textwrap.dedent("""{0}
            SELECT *   
                WHERE {{ 
                ?Contractor a :contractorID;
                :hasName ?name;
                :hasTelephone ?phone;
                :hasEmail ?email;
                :hasCountry ?country;
                :hasTerritory ?territory;
                :hasPostalAddress ?address .
                filter(?Contractor=:{1}) .
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

    def delete_contractor_by_id(self, id):
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

    def get_all_contractors(self):
        query = textwrap.dedent("""{0}
            select *
            where{{  ?Contractor a :contractorID;
                :hasName ?name;
                :hasTelephone ?phone;
                :hasEmail ?email;
                :hasCountry ?country;
                :hasTerritory ?territory;
                :hasPostalAddress ?address .
        }}
        """).format(self.prefix())
        return query

    def get_term_by_id(self, id):
        query = textwrap.dedent("""{0}
            SELECT *   
                WHERE {{ 
                ?Term a :termID;
                 :hasTermTypes ?type;
                 dct:identifier ?contract;
                dct:description ?description .
                filter(?Term=:{1}) .
            }}""").format(self.prefix(), id)

        return query

    def get_term_type_by_id(self, id):
        query = textwrap.dedent("""{0}
            SELECT *   
                WHERE {{ 
                ?TermType a :termTypeID;
                :hasName ?name;
                dct:description ?description .
                filter(?TermType=:{1}) .
            }}""").format(self.prefix(), id)

        return query

    def get_all_term_types(self):
        query = textwrap.dedent("""{0}
            select *
            where{{  ?TermType a :termTypeID;
                :hasName ?name;
                dct:description ?description .
        }}
        """).format(self.prefix())
        return query

    def get_all_terms(self):
        query = textwrap.dedent("""{0}
            select *
            where{{  ?Term a :termID;
                 :hasTermTypes ?type;
                 dct:identifier ?contract;
                dct:description ?description .
        }}
        """).format(self.prefix())
        return query

    def delete_term_by_id(self, id):
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

    def delete_term_type_by_id(self, id):
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

    def get_contract_obligations(self, id):
        query = textwrap.dedent("""{0}
            SELECT *
                WHERE {{
                ?Contract a :contractID;
                    :hasObligations ?obl .
                    ?obl :hasStates ?state .
                    ?obl dct:description ?obl_desc .
                    ?obl fibo-fnd-agr-ctr:hasExecutionDate ?exe_date .
                    ?obl :hasEndDate ?end_date .
                filter(?Contract=:{1}) .
            }}""").format(self.prefix(), id)

        return query

    def get_contract_terms(self, id):
        query = textwrap.dedent("""{0}
            SELECT *
                WHERE {{
                ?Contract a :contractID;
                    :hasTerms ?term .
                    ?term dct:description ?description .
                filter(?Contract=:{1}) .
            }}""").format(self.prefix(), id)
        return query

    def get_contract_contractors(self, id):
        query = textwrap.dedent("""{0}
            SELECT *
                WHERE {{
                ?Contract a :contractID;
                     :hasContractors ?contractor.
                ?contractor :hasName ?name .
                ?contractor :hasPostalAddress ?address .
                ?contractor :hasEmail ?email .
                ?contractor :hasTelephone ?phone .
                ?contractor :hasCountry ?country .
                ?contractor :hasTerritory ?territory .
                filter(?Contract=:{1}) .
            }}""").format(self.prefix(), id)
        return query

    def get_all_obligations(self):
        query = textwrap.dedent("""{0}
            select *
            where{{  
             ?Obligation a :obligationID;
                dct:description ?description;
                fibo-fnd-agr-ctr:hasExecutionDate ?executiondate;
                :hasEndDate ?enddate;
                :hasStates ?state .
        }}
        """).format(self.prefix())
        return query

    def get_contract_compliance(self):
        query = textwrap.dedent("""{0}
            select ?Obligation ?state ?obl_desc ?exe_date ?end_date ?identifier
            where{{  
            ?Obligation a ?oid;
           :hasStates ?state;
    		dct:description ?obl_desc;
    		fibo-fnd-agr-ctr:hasExecutionDate ?exe_date;
    		:hasEndDate ?end_date;
      		dct:identifier ?identifier .
        }}
        """).format(self.prefix())
        return query

    def delete_obligation_by_id(self, id):
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

    def get_obligation_by_id(self, id):
        query = textwrap.dedent("""{0}
            SELECT *   
                WHERE {{ 
                ?Obligation a :obligationID;
                    dct:description ?description;
                    fibo-fnd-agr-ctr:hasExecutionDate ?executiondate;
                    :hasEndDate ?enddate;
                    :hasStates ?state .
                filter(?Obligation=:{1}) .
            }}""").format(self.prefix(), id)

        return query

    def get_obligation_identifier_by_id(self, id):
        query = textwrap.dedent("""{0}
            SELECT ?identifier   
                WHERE {{ 
                 ?Obligation a :obligationID;
                dct:identifier ?identifier;
                filter(?Obligation=:{1}) .
            }}""").format(self.prefix(), id)

        return query

    def contract_update_status(self, id):
        violation_date = date.today()
        query = textwrap.dedent("""{0}
            DELETE {{?ContractId :hasContractStatus :hasCreated.
                    ?ContractId :hasContractStatus :hasPending.
                    ?ContractId :hasContractStatus :hasRenewed.}}
            INSERT {{?ContractId :hasContractStatus :hasViolated.
            ?ContractId :RevokedAtTime {1}.
            }}
             WHERE {{
             ?ContractId a :<http://ontologies.atb-bremen.de/smashHitCore#contractID>.
              FILTER(?ContractId = :{2})}}""").format(self.prefix(), '\'{}^^xsd:dateTime\''.format(violation_date), id)

        # print(query)
        return query

    def insert_query(self, ContractId, ContractType, Purpose,
                     EffectiveDate, ExecutionDate, EndDate, Medium, ContractStatus, ContractCategory,
                     ConsiderationDescription, ConsiderationValue, Contractors, Terms, Obligations):
        insquery = textwrap.dedent("""{0} 
            INSERT DATA {{
            :{1} a <http://ontologies.atb-bremen.de/smashHitCore#contractID>;
                       :contractType :{2};
                       :forPurpose "{3}";
                        fibo-fnd-agr-ctr:hasEffectiveDate :{4};
                        fibo-fnd-agr-ctr:hasExecutionDate :{5};
                        :hasEndDate :{6};
                        :inMedium "{7}";
                        :hasContractStatus :{8};
                        :hasContractCategory :{9};
                        dct:description "{10}";
                        rdf:value {11};
                         {12};
                         {13};
                         {14} .
                   }}       
               
          """.format(self.prefix(), ContractId, ContractType, Purpose,
                     EffectiveDate, ExecutionDate, EndDate, Medium, ContractStatus, ContractCategory,
                     ConsiderationDescription, ConsiderationValue, Contractors, Terms, Obligations))

        return insquery

    def insert_query_contractor(self, ContractorId, Name, Email, Phone, Address, Territory, Country, Role):
        insquery = textwrap.dedent("""{0} 
        INSERT DATA {{
            :{1} a <http://ontologies.atb-bremen.de/smashHitCore#contractorID>;
                        :hasName "{2}";
                        :hasEmail "{3}";
                        :hasTelephone "{4}";
                        :hasPostalAddress "{5}";
                        :hasTerritory "{6}";
                        :hasCountry "{7}";
                        :hasRole "{8}" .
                   }}       
          """.format(self.prefix(), ContractorId, Name, Email, Phone, Address, Territory, Country, Role))
        return insquery

    def insert_query_term(self, TermId, TermTypeId,ContractId, Description):
        insquery = textwrap.dedent("""{0} 
        INSERT DATA {{
            :{1} a <http://ontologies.atb-bremen.de/smashHitCore#termID>;
                        :hasTermTypes :{2};
                        dct:identifier :{3};
                        dct:description "{4}" .
                   }}       
          """.format(self.prefix(), TermId, TermTypeId, ContractId, Description))
        return insquery

    def insert_query_term_type(self, TermTypeId, Name, Description):
        insquery = textwrap.dedent("""{0} 
        INSERT DATA {{
            :{1} a <http://ontologies.atb-bremen.de/smashHitCore#termTypeID>;
                        :hasName "{2}";
                        dct:description "{3}" .
                   }}       
          """.format(self.prefix(), TermTypeId, Name, Description))
        return insquery

    def insert_query_obligation(self, ObligationId, Description, TermId, ContractorId, ContractId, State, ExecutionDate,
                                EndDate):
        insquery = textwrap.dedent("""{0} 
        INSERT DATA {{
            :{1} a <http://ontologies.atb-bremen.de/smashHitCore#obligationID>;
                        dct:description "{2}";
                        dct:identifier :{3};
                        dct:identifier :{4};
                        dct:identifier :{5};
                        :hasStates :{6};
                        fibo-fnd-agr-ctr:hasExecutionDate :{7};
                        :hasEndDate :{8} .
                   }}       
          """.format(self.prefix(), ObligationId, Description, TermId, ContractorId, ContractId, State, ExecutionDate,
                     EndDate))
        return insquery
