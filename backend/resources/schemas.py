from resources.imports import *


class NestedSchema(Schema):
    Contract = fields.Dict(
        required=True, keys=fields.Str(),
        values=fields.Str()
    )


class ForNestedSchema(Schema):
    data = fields.List(fields.String())


class GenerateToken(MethodResource, Resource):
    # check username and password
    def check_for_username_password(func):
        @wraps(func)
        def wrapped(*args, **kwargs):

            username = os.getenv('uname')
            password = os.getenv('upass')
            secret_key = os.getenv('SECRET_KEY')

            print(request.authorization)
            print(request.headers)

            if request.authorization and request.authorization.Username and request.authorization.Password:
                if request.authorization.Username == username and request.authorization.Password == password:
                    token = jwt.encode({
                        'username': username,
                        'exp': datetime.utcnow() + timedelta(minutes=1)
                    }, secret_key)
                    return jsonify({'token': token.decode('UTF-8')})
                else:
                    return 'username or password is not correct'
            elif request.headers.get('Username') and request.headers.get('Password'):
                if request.headers.get('Username') == username and request.headers.get('Password') == password:
                    token = jwt.encode({
                        'username': username,
                        'exp': datetime.utcnow() + timedelta(minutes=1)
                    }, secret_key)
                    return jsonify({'token': token.decode('UTF-8')})
                else:
                    return 'username or password is not correct'
            else:
                return 'Basic authentication is required.'

        return wrapped

    @check_for_username_password
    def get(self):
        return True


class ObligationRequestSchema(Schema):
    Description = fields.String(required=True, description="Description")
    TermId = fields.String(required=True, description="Term ID")
    ContractorId = fields.String(required=True, description="Contractor ID")
    ContractId = fields.String(required=True, description="Contract ID")
    ContractIdB2C = fields.String(required=False, description="Contract ID B2C")
    State = fields.String(required=False, description="Obligation State")
    ExecutionDate = fields.DateTime(required=False, description="Execution Date")
    EndDate = fields.DateTime(required=False, description="End Date")


class ObligationUpdateSchema(Schema):
    ObligationId = fields.String(required=True, description="Obligation ID")
    Description = fields.String(required=True, description="Description")
    TermId = fields.String(required=True, description="Term ID")
    ContractorId = fields.String(required=True, description="Contractor ID")
    ContractId = fields.String(required=True, description="Contract ID")
    ContractIdB2C = fields.String(required=False, description="Contract ID B2C")
    State = fields.String(required=False, description="Obligation State")
    ExecutionDate = fields.DateTime(required=False, description="Execution Date")
    EndDate = fields.DateTime(required=False, description="End Date")


class ContractorRequestSchema(Schema):
    Name = fields.String(required=True, description="Name")
    Email = fields.String(required=True, description="Email")
    Phone = fields.String(required=True, description="Phone Number")
    Address = fields.String(required=True, description="Street Address")
    Territory = fields.String(required=False, description="Territory")
    Country = fields.String(required=False, description="Country")
    Role = fields.String(required=True, description="Role")
    Vat = fields.String(required=False, description="Vat")
    CompanyId = fields.String(required=False, description="Company ID")
    CreateDate = fields.DateTime(required=False, description="Create Date")


class ContractorUpdateSchema(Schema):
    ContractorId = fields.String(required=True, description="Contractor ID")
    Name = fields.String(required=True, description="Name")
    Email = fields.String(required=True, description="Email")
    Phone = fields.String(required=True, description="Phone Number")
    Address = fields.String(required=True, description="Street Address")
    Territory = fields.String(required=False, description="Territory")
    Country = fields.String(required=False, description="Country")
    Role = fields.String(required=True, description="Role")
    Vat = fields.String(required=False, description="Vat")
    CompanyId = fields.String(required=False, description="Company ID")
    CreateDate = fields.DateTime(required=False, description="Create Date")


class CompanyRequestSchema(Schema):
    Name = fields.String(required=True, description="Name")
    Email = fields.String(required=True, description="Email")
    Phone = fields.String(required=True, description="Phone Number")
    Address = fields.String(required=True, description="Street Address")
    Territory = fields.String(required=False, description="Territory")
    Country = fields.String(required=False, description="Country")
    Vat = fields.String(required=False, description="VAT")
    CreateDate = fields.DateTime(required=False, description="Create Date")


class CompanyUpdateSchema(Schema):
    CompanyId = fields.String(required=True, description="Company ID")
    Name = fields.String(required=True, description="Name")
    Email = fields.String(required=True, description="Email")
    Phone = fields.String(required=True, description="Phone Number")
    Address = fields.String(required=True, description="Street Address")
    Territory = fields.String(required=False, description="Territory")
    Country = fields.String(required=False, description="Country")
    Vat = fields.String(required=False, description="VAT")
    CreateDate = fields.DateTime(required=False, description="Create Date")


class TermTypeUpdateSchema(Schema):
    TermTypeId = fields.String(required=True, description="TermId")
    Name = fields.String(required=False, description="Name")
    Description = fields.String(required=False, description="Description")
    CreateDate = fields.DateTime(required=False, description="Create Date")


class TermTypeRequestSchema(Schema):
    Name = fields.String(required=False, description="Name")
    Description = fields.String(required=False, description="Description")
    CreateDate = fields.DateTime(required=False, description="Create Date")


class TermUpdateSchema(Schema):
    TermId = fields.String(required=True, description="TermId")
    TermTypeId = fields.String(required=True, description="TermTypeId")
    ContractId = fields.String(required=True, description="Contract ID")
    Description = fields.String(required=False, description="Description")
    CreateDate = fields.DateTime(required=False, description="Create Date")


class TermRequestSchema(Schema):
    TermTypeId = fields.String(required=True, description="TermTypeId")
    ContractId = fields.String(required=True, description="Contract ID")
    Description = fields.String(required=False, description="Description")
    CreateDate = fields.DateTime(required=False, description="Create Date")


class ContractUpdateSchema(Schema):
    ContractId = fields.String(required=True, description="Contract ID")
    ConsentId = fields.String(required=False, description="Consent ID")
    ContractType = fields.String(required=True,
                                 description="Contract Type")
    Purpose = fields.String(required=True, description="For What Purpose")

    ExecutionDate = fields.DateTime(required=False,
                                    description="Execution Date")
    EffectiveDate = fields.DateTime(required=False,
                                    description="Effective Date")
    EndDate = fields.DateTime(required=False,
                              description="Expire Date")
    Medium = fields.String(required=False, description="Medium")

    ContractStatus = fields.String(
        required=False, description="Contract Status")

    ConsiderationDescription = fields.String(
        required=False, description="Consideration description")
    ConsiderationValue = fields.String(
        required=False, description="Consideration Value")
    ContractCategory = fields.String(
        required=False, description="Contract Category")
    Contractors = fields.List(fields.String(),
                              required=False, description="Contractors")
    Terms = fields.List(fields.String(),
                        required=False, description="Contract Terms")
    Obligations = fields.List(fields.String(),
                              required=False, description="Contract Obligations")
    Signatures = fields.List(fields.String(),
                             required=False, description="Contractor Signatures")


class ContractRequestSchema(Schema):
    ConsentId = fields.String(required=False, description="Consent ID")
    ContractType = fields.String(required=True,
                                 description="Contract Type")
    Purpose = fields.String(required=True, description="For What Purpose")

    ExecutionDate = fields.DateTime(required=False,
                                    description="Execution Date")
    EffectiveDate = fields.DateTime(required=False,
                                    description="Effective Date")
    EndDate = fields.DateTime(required=False,
                              description="Expire Date")
    Medium = fields.String(required=False, description="Medium")

    ContractStatus = fields.String(
        required=False, description="Contract Status")

    ContractCategory = fields.String(
        required=False, description="Contract Category")

    ConsiderationDescription = fields.String(
        required=False, description="Consideration description")
    ConsiderationValue = fields.String(
        required=False, description="Consideration Value")
    Contractors = fields.List(fields.String(),
                              required=False, description="Contractors")
    Terms = fields.List(fields.String(),
                        required=False, description="Contract Terms")
    Obligations = fields.List(fields.String(),
                              required=False, description="Contract Obligations")
    Signatures = fields.List(fields.String(),
                             required=False, description="Contractor Signatures")


class ContractorSignaturesRequestSchema(Schema):
    ContractId = fields.String(required=True, description="Contract ID")
    ContractorId = fields.String(required=True, description="Contractor ID")
    CreateDate = fields.Date(required=False, description="Create Date")
    Signature = fields.String(required=True, description="Signature")


class ContractorSignaturesUpdateSchema(Schema):
    SignatureId = fields.String(required=True, description="Signature ID")
    ContractId = fields.String(required=True, description="Contract ID")
    ContractorId = fields.String(required=True, description="Contractor ID")
    CreateDate = fields.DateTime(required=False, description="Create Date")
    Signature = fields.String(required=True, description="Signature")


class BulkResponseQuerySchema(Schema):
    bindings = fields.List(fields.Nested(NestedSchema), required=True)
