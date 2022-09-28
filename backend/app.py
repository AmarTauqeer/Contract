import datetime

from flask import Flask
from apispec import APISpec
from flask_apispec.extension import FlaskApiSpec
from apispec.ext.marshmallow import MarshmallowPlugin
from resources.contracts import *
from resources.users import RegisterUser, Login, Logout, DeleteUser, AllUsers
from resources.contractors import *
from resources.company import *
from resources.contract_terms import *
from resources.contract_obligation import *
from resources.term_types import *
from resources.contract_compliance import *
from resources.contract_signatures import *
from tests.contract_test import *
from flask_restful import Api
from flask_cors import CORS
from flask_migrate import Migrate
from flask_session import Session
from core.config import ApplicationConfig
from flask_bcrypt import Bcrypt
from core.models import User, db
from flask_swagger_ui import get_swaggerui_blueprint

from flask_apscheduler import APScheduler
import time
import requests

# from resources.users import Register,Logout

app = Flask(__name__)
scheduler = APScheduler()
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
cors = CORS(app, resources={
    r"/contract/*": {
        "origins": "*"
    }
}, supports_credentials=True)

# swagger configuration

SWAGGER_URL = '/swagger-ui'
API_URL = '/static/swagger.json'
SWAGGER_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "smashHit Contracting API"
    }
)
app.register_blueprint(SWAGGER_BLUEPRINT, url_prefix=SWAGGER_URL)
# authorizations = {"Bearer": {"type": "apiKey", "in": "header", "name": "Authorization"}}

# app.config.update({
#     'APISPEC_SPEC': APISpec(
#         title='Automatic Contracting Tool Contracts API Specification',
#         info=dict(description="Author: Amar Tauqeer, Email: amar.tauqeer@sti2.at"),
#         version='v001',
#         plugins=[MarshmallowPlugin()],
#         openapi_version='2.0.0',
#         # authorizations=authorizations,
#     )
#     ,
#     'APISPEC_SWAGGER_UI_URL': '/swagger-ui/',
#
# })

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
# docs.register(GenerateToken)

api.add_resource(RegisterUser, '/contract/register/')
docs.register(RegisterUser)

api.add_resource(Login, '/contract/login/')
docs.register(Login)

# api.add_resource(Logout, '/contract/logout/')
# docs.register(Logout)

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


api.add_resource(Contracts, '/contract/list_of_contracts/')
docs.register(Contracts)

api.add_resource(ContractByContractor,
                 '/contract/byContractor/<string:contractorID>/')
docs.register(ContractByContractor)

api.add_resource(ContractByContractId,
                 '/contract/byContract/<string:contractID>/')
docs.register(ContractByContractId)

api.add_resource(ContractorById,
                 '/contract/contractor/<string:contractorID>/')
docs.register(ContractorById)

api.add_resource(CompanyById,
                 '/contract/company/<string:companyID>/')
docs.register(CompanyById)

api.add_resource(ContractDeleteById,
                 '/contract/delete/<string:contractID>/')
docs.register(ContractDeleteById)

api.add_resource(ContractorDeleteById,
                 '/contract/contractor/delete/<string:contractorID>/')
docs.register(ContractorDeleteById)

api.add_resource(CompanyDeleteById,
                 '/contract/company/delete/<string:companyID>/')
docs.register(CompanyDeleteById)

api.add_resource(ContractCreate, '/contract/create/')
docs.register(ContractCreate)

api.add_resource(ContractorCreate, '/contract/contractor/create/')
docs.register(ContractorCreate)

api.add_resource(CompanyCreate, '/contract/company/create/')
docs.register(CompanyCreate)

api.add_resource(ContractUpdate, '/contract/update/')
docs.register(ContractUpdate)

api.add_resource(ContractorUpdate, '/contract/contractor/update/')
docs.register(ContractorUpdate)

api.add_resource(CompanyUpdate, '/contract/company/update/')
docs.register(CompanyUpdate)

api.add_resource(GetContractors, '/contract/contractors/')
docs.register(GetContractors)

api.add_resource(GetCompany, '/contract/companies/')
docs.register(GetCompany)

api.add_resource(GetTermTypes, '/contract/term/types')
docs.register(GetTermTypes)

api.add_resource(GetTerms, '/contract/terms/')
docs.register(GetTerms)

api.add_resource(GetContractSignatures, '/contract/signatures/<string:contractID>')
docs.register(GetContractSignatures)

api.add_resource(GetSignatures, '/contract/signatures/')
docs.register(GetSignatures)

api.add_resource(GetObligations, '/contract/obligations/')
docs.register(GetObligations)

api.add_resource(TermUpdate, '/contract/term/update/')
docs.register(TermUpdate)

api.add_resource(TermCreate, '/contract/term/create/')
docs.register(TermCreate)

api.add_resource(ContractSignatureCreate, '/contract/signature/create/')
docs.register(ContractSignatureCreate)

api.add_resource(ContractSignatureUpdate, '/contract/signature/update/')
docs.register(ContractSignatureUpdate)

api.add_resource(SignatureById,
                 '/contract/signature/<string:signatureID>/')
docs.register(SignatureById)

api.add_resource(SignatureDeleteById,
                 '/contract/signature/delete/<string:signatureID>/')
docs.register(SignatureDeleteById)

api.add_resource(TermTypeUpdate, '/contract/term/type/update/')
docs.register(TermTypeUpdate)

api.add_resource(TermTypeCreate, '/contract/term/type/create/')
docs.register(TermTypeCreate)

api.add_resource(TermDeleteById,
                 '/contract/term/delete/<string:termID>/')
docs.register(TermDeleteById)

api.add_resource(TermTypeDeleteById,
                 '/contract/term/type/delete/<string:termTypeID>/')
docs.register(TermTypeDeleteById)

api.add_resource(TermTypeById,
                 '/contract/termType/<string:termTypeID>/')
docs.register(TermTypeById)

api.add_resource(TermById,
                 '/contract/term/<string:termID>/')
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
                 '/contract/obligation/<string:obligationID>/')
docs.register(ObligationById)

api.add_resource(ObligationCreate, '/contract/obligation/create/')
docs.register(ObligationCreate)

api.add_resource(ObligationDeleteById,
                 '/contract/obligation/delete/<string:obligationID>/')
docs.register(ObligationDeleteById)

api.add_resource(GetObligationIdentifierById,
                 '/contract/obligation/identifier/<string:obligationID>/')
docs.register(GetObligationIdentifierById)

api.add_resource(ObligationStatusUpdateByObligationId,
                 '/contract/obligation/status/<string:obligationID>/<string:contractID>/<string:contractorID>/<string:state>/')
docs.register(ObligationStatusUpdateByObligationId)

api.add_resource(ContractStatusUpdateById,
                 '/contract/status/<string:contractID>/<string:status>/')
docs.register(ContractStatusUpdateById)

api.add_resource(GetContractCompliance, '/contract/compliance/')
docs.register(GetContractCompliance)

# api.add_resource(ContractApiTest.test_get_all_contracts, '/contract/tests/')
# docs.register(ContractApiTest.test_get_all_contracts)

# contract compliance schedule
# current_date = date(2022, 4, 26)

current_date = date.today()


def compliance():
    CONTRACT_URL = "https://actool.contract.sti2.at/contract/compliance/"
    # CONTRACT_URL = "http://172.25.0.81:5000/contract/compliance/"
    data = requests.get(CONTRACT_URL)
    data = data.json()


if __name__ == '__main__':
    # scheduler.add_job(id='Contract compliance task', func=compliance, trigger='interval', minutes=1440)
    # if current_date >= date(2022, 4, 26):
    #     scheduler.start()
    app.run(debug=True, host='0.0.0.0', port=5002)
