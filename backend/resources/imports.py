import textwrap

import smtplib
import uuid

from core.storage.Sparql import SPARQL
from SPARQLWrapper import JSON, SPARQLWrapper, BASIC
from flask import json, jsonify
from flask_restful import Resource, request
from flask_apispec.views import MethodResource
from flask_apispec import marshal_with, doc, use_kwargs
from marshmallow import Schema, fields
from functools import wraps
import jwt
import os
import re
from datetime import *
from datetime import datetime, timedelta
from core.query_processor.QueryProcessor import QueryEngine
from core.contract_validation.ContractValidation import ContractValidation
from core.contractor_validation.ContractorValidation import ContractorValidation
from core.company_validation.CompanyValidation import CompanyValidation
from core.term_validation.term_validation import TermValidation
from core.obligation_validation.obligation_validation import ObligationValidation
from core.term_type_validation.term_type_validation import TermTypeValidation
# from tests.contract_test import ContractApiTest
import unittest
from core.Credentials import Credentials

from resources.users import check_for_session