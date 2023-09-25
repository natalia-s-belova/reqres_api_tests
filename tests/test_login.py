import jsonschema
from utils import helper

service = "regres"


def test_login_response_schema():
    response = helper.api_request(
        service,
        "post",
        url="/api/login",
        data={"email": "eve.holt@reqres.in", "password": "cityslicka"}
    )
    schema = helper.response_schema(helper.path_dir('resources', 'post_successful_login_schema.json'))

    assert response.status_code == 200
    jsonschema.validators.validate(instance=response.json(), schema=schema)


def test_successful_login():
    response = helper.api_request(
        service,
        "post",
        url="/api/login",
        data={"email": "eve.holt@reqres.in", "password": "cityslicka"}
    )

    assert response.status_code == 200
    assert response.json()["token"] == "QpwL5tke4Pnpja7X4"


def test_failed_login_non_existing_user():
    response = helper.api_request(
        service,
        "post",
        url="/api/login",
        data={"email": "eve.holtNEW@reqres.in", "password": "cityslicka"}
    )

    assert response.status_code == 400
    assert response.json()["error"] == "user not found"


def test_failed_login_non_specified_password():
    response = helper.api_request(
        service,
        "post",
        url="/api/login",
        data={"email": "eve.holt@reqres.in", "password": ""}
    )

    assert response.status_code == 400
    assert response.json()["error"] == "Missing password"
