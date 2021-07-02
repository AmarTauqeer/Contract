from flask import Flask
from apispec import APISpec
from flask_apispec.extension import FlaskApiSpec
from apispec.ext.marshmallow import MarshmallowPlugin
from resources.contracts import Contracts, ContractByRequester, \
    ContractByProvider, ContractByContractId, ContractCreate,\
    GenerateToken
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
        title='Automatic Contracting API Specification',
        version='v01',
        plugins=[MarshmallowPlugin()],
        openapi_version='2.0.0'
    ),
    'APISPEC_SWAGGER_UI_URL': '/',
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
api.add_resource(ContractCreate, '/contract/create/')
docs.register(ContractCreate)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
