from reqres_api_tests.utils import helper
from reqres_api_tests.models import reqres
import allure
from allure_commons.types import Severity


pytestmark = [
    allure.label('layer', 'API test'),
    allure.label('owner', 'natalia_belova'),
    allure.epic('Reqres API'),
    allure.tag('REST')
]


@allure.title('Verify response schema for Login')
@allure.feature('Login')
@allure.story('Login')
@allure.severity(Severity.CRITICAL)
def test_login_response_schema():
    response = helper.api_request(
        "post",
        url="/api/login",
        data={"email": "eve.holt@reqres.in", "password": "cityslicka"}
    )

    reqres.verify_code(response, 200)
    reqres.verify_schema(response, 'post_login.json')


@allure.title('Verify response content for successful Login')
@allure.feature('Login')
@allure.story('Login')
@allure.severity(Severity.BLOCKER)
def test_successful_login():
    response = helper.api_request(
        "post",
        url="/api/login",
        data={"email": "eve.holt@reqres.in", "password": "cityslicka"}
    )

    reqres.verify_code(response, 200)
    reqres.verify_response_json(response, 'token', 'QpwL5tke4Pnpja7X4')


@allure.title('Verify error for failed Login - user does not exist')
@allure.feature('Login')
@allure.story('Login')
@allure.severity(Severity.CRITICAL)
def test_failed_login_non_existing_user():
    response = helper.api_request(
        "post",
        url="/api/login",
        data={"email": "eve.holtNEW@reqres.in", "password": "cityslicka"}
    )

    reqres.verify_code(response, 400)
    reqres.verify_response_json(response, 'error', 'user not found')


@allure.title('Verify error for failed Login - password is not provided')
@allure.feature('Login')
@allure.story('Login')
@allure.severity(Severity.CRITICAL)
def test_failed_login_non_specified_password():
    response = helper.api_request(
        "post",
        url="/api/login",
        data={"email": "eve.holt@reqres.in", "password": ""}
    )

    reqres.verify_code(response, 400)
    reqres.verify_response_json(response, 'error', 'Missing password')


@allure.title('Verify error for not well-formed json for Login')
@allure.feature('Login')
@allure.story('Login')
@allure.severity(Severity.NORMAL)
def test_failed_login_non_well_formed_json():
    response = helper.api_request(
        "post",
        url="/api/login",
        headers={'Content-Type': 'application/json'},
        data="{\"email\": \"eve.holt@reqres.in\" \"password: \"pistol\"}"
    )

    reqres.verify_code(response, 400)
    reqres.verify_response_text(response, 'Bad Request')
