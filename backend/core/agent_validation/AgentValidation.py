from core.query_processor.QueryProcessor import QueryEngine
from flask import jsonify


class AgentValidation(QueryEngine):

    def __init__(self):
        super().__init__()

    def delete_agent(self, agentId):
        response = self.post_sparql(self.get_username(), self.get_password(), self.delete_agent_by_id(agentId))
        return response

    def post_data(self, validated_data, type):
        AgentId = validated_data["AgentId"]
        AgentType = validated_data["AgentType"]
        Name = validated_data["Name"]
        Email = validated_data["Email"]
        Phone = validated_data["Phone"]
        Address = validated_data["Address"]
        City = validated_data["City"]
        State = validated_data["State"]
        Country = validated_data["Country"]

        if type == "insert":
            respone = self.post_sparql(self.get_username(), self.get_password(),
                                       self.insert_query_agent(AgentId=AgentId,
                                                               AgentType=AgentType,
                                                               Name=Name,
                                                               Email=Email,
                                                               Phone=Phone,
                                                               Address=Address,
                                                               City=City,
                                                               State=State,
                                                               Country=Country,
                                                               )

                                       )
        else:
            if AgentId != "":
                # delete from knowledge graph
                response = self.post_sparql(self.get_username(), self.get_password(),
                                            self.delete_agent_by_id(AgentId))

                # insert into kg
                respone = self.post_sparql(self.get_username(), self.get_password(),
                                           self.insert_query_agent(AgentId=AgentId,
                                                             AgentType=AgentType,
                                                             Name=Name,
                                                             Email=Email,
                                                             Phone=Phone,
                                                             Address=Address,
                                                             City=City,
                                                             State=State,
                                                             Country=Country,
                                                             )

                                           )
        return respone
