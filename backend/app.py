from flask import Flask
from apispec import APISpec
from flask_apispec.extension import FlaskApiSpec
from apispec.ext.marshmallow import MarshmallowPlugin
from resources.contracts import Contracts, ContractByRequester, \
    ContractByProvider, ContractByContractId, ContractCreate, \
    GenerateToken, ContractUpdate, ContractDeleteById, GetContractors, \
    ContractorDeleteById, ContractorCreate, ContractorById, ContractorUpdate, \
    GetTerms, TermUpdate, TermCreate, TermById, TermDeleteById, GetObligationByContractId, \
    GetContractTerms, GetContractContractors,GetObligations, ObligationById, ObligationCreate, \
ObligationDeleteById
from resources.users import RegisterUser, Login, Logout, DeleteUser, AllUsers
from flask_restful import Api
from flask_cors import CORS
from flask_migrate import Migrate
from flask_session import Session
from core.config import ApplicationConfig
from flask_bcrypt import Bcrypt
from core.models import User, db

# from resources.users import Register,Logout

app = Flask(__name__)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
cors = CORS(app, resources={
    r"/contract/*": {
        "origins": "*"
    }
}, supports_credentials=True)
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
app.config.from_object(ApplicationConfig)
server_session = Session(app)
db.init_app(app)

with app.app_context():
    db.create_all()

api = Api(app)
docs = FlaskApiSpec(app)
# token
# generate token
api.add_resource(GenerateToken, '/contract/token/')

# api.add_resource(RegisterUser, '/contract/register/')
# docs.register(RegisterUser)
#
# api.add_resource(DeleteUser, '/contract/delete_user/<string:email>/')
# docs.register(DeleteUser)
#
# api.add_resource(AllUsers, '/contract/get_all_user/')
# docs.register(AllUsers)
#
# api.add_resource(Login, '/contract/login/')
# docs.register(Login)
#
# api.add_resource(Logout, '/contract/logout/')
# docs.register(Logout)

api.add_resource(Contracts, '/contract/list_of_contracts/')
docs.register(Contracts)

# api.add_resource(ContractByRequester,
#                  '/contract/by_requester/<string:requester>/')
# docs.register(ContractByRequester)
#
# api.add_resource(ContractByProvider,
#                  '/contract/by_provider/<string:provider>/')
# docs.register(ContractByProvider)

api.add_resource(ContractByContractId,
                 '/contract/by_contractId/<string:contractID>/')
docs.register(ContractByContractId)

api.add_resource(ContractorById,
                 '/contractor/by_contractorId/<string:contractorID>/')
docs.register(ContractorById)

api.add_resource(ContractDeleteById,
                 '/contract/delete/<string:contractID>/')
docs.register(ContractDeleteById)

api.add_resource(ContractorDeleteById,
                 '/contractor/delete/<string:contractorID>/')
docs.register(ContractorDeleteById)

api.add_resource(ContractCreate, '/contract/create/')
docs.register(ContractCreate)

api.add_resource(ContractorCreate, '/contractor/create/')
docs.register(ContractorCreate)

api.add_resource(ContractUpdate, '/contract/update/')
docs.register(ContractUpdate)

api.add_resource(ContractorUpdate, '/contractor/update/')
docs.register(ContractorUpdate)

api.add_resource(GetContractors, '/contractors/')
docs.register(GetContractors)

api.add_resource(GetTerms, '/terms/')
docs.register(GetTerms)

api.add_resource(GetObligations, '/obligations/')
docs.register(GetObligations)

api.add_resource(TermUpdate, '/term/update/')
docs.register(TermUpdate)

api.add_resource(TermCreate, '/term/create/')
docs.register(TermCreate)

api.add_resource(TermDeleteById,
                 '/term/delete/<string:termID>/')
docs.register(TermDeleteById)

api.add_resource(TermById,
                 '/term/by_termId/<string:termID>/')
docs.register(TermById)

api.add_resource(GetObligationByContractId,
                 '/contract/obligations/<string:contractID>/')
docs.register(GetObligationByContractId)

api.add_resource(GetContractTerms,
                 '/contract/terms/<string:contractID>/')
docs.register(GetContractTerms)

api.add_resource(GetContractContractors,
                 '/contract/contractors/<string:contractID>/')
docs.register(GetContractContractors)

api.add_resource(ObligationById,
                 '/obligation/by_obligationId/<string:obligationID>/')
docs.register(ObligationById)

api.add_resource(ObligationCreate, '/obligation/create/')
docs.register(ObligationCreate)

api.add_resource(ObligationDeleteById,
                 '/obligation/delete/<string:obligationID>/')
docs.register(ObligationDeleteById)
# api.add_resource(GetContractTestResult, '/contract/tests/')
# docs.register(GetContractTestResult)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
