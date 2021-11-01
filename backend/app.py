from flask import Flask
from apispec import APISpec
from flask_apispec.extension import FlaskApiSpec
from apispec.ext.marshmallow import MarshmallowPlugin
from resources.contracts import Contracts, ContractByRequester, \
    ContractByProvider, ContractByContractId, ContractCreate, \
    GenerateToken, ContractUpdate, ContractDeleteById,GetAgents, \
    AgentDeleteById,AgentCreate,AgentByAgentId
from flask_restful import Api
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={
    r"/contract/*": {
        "origins": "*"
    }
})
# swagger configuration
app.config.update({
    'APISPEC_SPEC': APISpec(
        title='Contracts API Specification',
        version='v01',
        plugins=[MarshmallowPlugin()],
        openapi_version='2.0.0'
    ),
    'APISPEC_SWAGGER_UI_URL': '/swagger-ui/',
})

api = Api(app)
docs = FlaskApiSpec(app)
# token
# generate token
api.add_resource(GenerateToken, '/contract/token/')

api.add_resource(Contracts, '/contract/list_of_contracts/')
docs.register(Contracts)
api.add_resource(ContractByRequester,
                 '/contract/by_requester/<string:requester>/')
docs.register(ContractByRequester)
api.add_resource(ContractByProvider,
                 '/contract/by_provider/<string:provider>/')
docs.register(ContractByProvider)

api.add_resource(ContractByContractId,
                 '/contract/by_contractId/<string:contractId>/')
docs.register(ContractByContractId)

api.add_resource(AgentByAgentId,
                 '/agent/by_agentId/<string:agentId>/')
docs.register(AgentByAgentId)

api.add_resource(ContractDeleteById,
                 '/contract/delete/<string:contractId>/')
docs.register(ContractDeleteById)

api.add_resource(AgentDeleteById,
                 '/Agent/delete/<string:agentId>/')
docs.register(AgentDeleteById)

api.add_resource(ContractCreate, '/contract/create/')
docs.register(ContractCreate)

api.add_resource(AgentCreate, '/Agent/create/')
docs.register(AgentCreate)

api.add_resource(ContractUpdate, '/contract/update/')
docs.register(ContractUpdate)

api.add_resource(GetAgents, '/contract/agents/')
docs.register(GetAgents)

# api.add_resource(GetContractTestResult, '/contract/tests/')
# docs.register(GetContractTestResult)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
