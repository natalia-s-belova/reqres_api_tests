import jsonschema
from reqres_api_tests.utils import helper

import allure
from allure_commons.types import Severity

pytestmark = [
    allure.label('layer', 'API test'),
    allure.label('owner', 'nsbelova'),
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
    schema = helper.response_schema(helper.path_dir('resources', 'schemas', 'post_login.json'))

    assert response.status_code == 200
    jsonschema.validators.validate(instance=response.json(), schema=schema)


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

    assert response.status_code == 200
    assert response.json()["token"] == "QpwL5tke4Pnpja7X4"


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

    assert response.status_code == 400
    assert response.json()["error"] == "user not found"


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

    assert response.status_code == 400
    assert response.json()["error"] == "Missing password"


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

    assert response.status_code == 400
    assert 'Bad Request' in response.text
