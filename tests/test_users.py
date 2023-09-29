import pytest
from reqres_api_tests.utils import helper
from reqres_api_tests.models import reqres
import allure
from allure_commons.types import Severity

pytestmark = [
    allure.label('layer', 'API test'),
    allure.label('owner', 'nsbelova'),
    allure.epic('Reqres API'),
    allure.tag('REST')
]


@allure.title('Verify response schema for Users List')
@allure.feature('Users List')
@allure.story('Get Users List')
@allure.severity(Severity.CRITICAL)
def test_users_list_response_schema():
    response = helper.api_request("get", url="/api/users")

    reqres.verify_code(response, 200)
    reqres.verify_schema(response, 'get_users_list.json')


@allure.title('Verify emails in the response for Users List when all users are requested')
@allure.feature('Users List')
@allure.story('Get Users List')
@allure.severity(Severity.CRITICAL)
def test_users_list_emails_are_correct_all_users_requested():
    per_page = 12
    registered_emails = ['george.bluth@reqres.in',
                         'janet.weaver@reqres.in',
                         'emma.wong@reqres.in',
                         'eve.holt@reqres.in',
                         'charles.morris@reqres.in',
                         'tracey.ramos@reqres.in',
                         'michael.lawson@reqres.in',
                         'lindsay.ferguson@reqres.in',
                         'tobias.funke@reqres.in',
                         'byron.fields@reqres.in',
                         'george.edwards@reqres.in',
                         'rachel.howell@reqres.in']

    response = helper.api_request("get", url="/api/users", params={"per_page": per_page})

    reqres.verify_code(response, 200)
    reqres.verify_response_json(response, 'total', per_page)

    reqres.verify_correct_values_for_parameter(response, 'email', registered_emails)


@allure.title('Verify last names in the response for Users List when per_page is specified and pagination applied')
@allure.feature('Users List')
@allure.story('Get Users List')
@allure.severity(Severity.CRITICAL)
def test_users_last_names_are_correct_and_pagination_applied():
    per_page = 4
    page_number = 3
    lastnames_shown = ['Funke', 'Fields', 'Edwards', 'Howell']

    response = helper.api_request("get", url="/api/users", params={"per_page": per_page, "page": page_number})

    reqres.verify_code(response, 200)
    reqres.verify_response_json(response, 'total', 12)
    reqres.verify_correct_values_for_parameter(response, 'last_name', lastnames_shown)


@allure.title('Verify response content for Users List when per_page is more than existing users')
@allure.feature('Users List')
@allure.story('Get Users List')
@allure.severity(Severity.NORMAL)
@pytest.mark.parametrize('per_page_amount', [20, 100])
def test_users_list_when_per_page_amount_more_than_existing_users(per_page_amount):
    per_page = per_page_amount

    response = helper.api_request("get", url="/api/users", params={"per_page": per_page})

    reqres.verify_code(response, 200)
    reqres.verify_response_json(response, 'per_page', per_page)
    reqres.verify_amount_users_shown(response, 12)


@allure.title('Verify response schema for Single User')
@allure.feature('Single User')
@allure.story('Get Single User Info')
@allure.severity(Severity.CRITICAL)
def test_user_single_response_schema():
    id = 7

    response = helper.api_request("get", url=f"/api/users/{id}")

    reqres.verify_code(response, 200)
    reqres.verify_schema(response, 'get_single_user.json')


@allure.title('Verify response content for Single User')
@allure.feature('Single User')
@allure.story('Get Single User Info')
@allure.severity(Severity.CRITICAL)
def test_single_existing_user_data():
    id = 8

    response = helper.api_request("get", url=f"/api/users/{id}")

    reqres.verify_code(response, 200)
    reqres.verify_response_json_data(response, 'id', id)
    reqres.verify_response_json_data(response, 'email', 'lindsay.ferguson@reqres.in')
    reqres.verify_response_json_data(response, 'first_name', 'Lindsay')
    reqres.verify_response_json_data(response, 'last_name', 'Ferguson')
    reqres.verify_response_json_data(response, 'avatar', 'https://reqres.in/img/faces/8-image.jpg')


@allure.title('Verify avatar for Single User')
@allure.feature('Single User')
@allure.story('Get Single User Info')
@allure.severity(Severity.CRITICAL)
@pytest.mark.parametrize('user_id', [7, 8, 9])
def test_single_user_avatar(user_id):
    id = user_id

    response = helper.api_request("get", url=f"/api/users/{id}")

    reference = helper.path_dir('resources', 'images', f'{id}.jpeg')
    actual = helper.path_dir('resources', 'images', 'downloaded.jpeg')
    helper.download_file_by_url_as(response.json()['data']['avatar'], actual)

    reqres.verify_code(response, 200)
    reqres.verify_avatar_as_referenced(actual, reference)

    helper.remove_file(actual)


@allure.title('Verify error when non-existing user requested')
@allure.feature('Single User')
@allure.story('Get Single User Info')
@allure.severity(Severity.CRITICAL)
def test_single_non_existing_user():
    id = 23

    response = helper.api_request("get", url=f"/api/users/{id}")

    reqres.verify_code(response, 404)
    reqres.verify_empty_response(response)


@allure.title('Verify response schema for Create User')
@allure.feature('Single User')
@allure.story('Post Single User')
@allure.severity(Severity.CRITICAL)
def test_create_user_response_schema():
    response = helper.api_request(
        "post",
        url="/api/users",
        data={"name": "morpheus", "job": "leader"}
    )

    reqres.verify_code(response, 201)
    reqres.verify_schema(response, 'post_user.json')


@allure.title('Verify response content for Create User')
@allure.feature('Single User')
@allure.story('Post Single User')
@allure.severity(Severity.CRITICAL)
def test_create_new_user():
    response = helper.api_request(
        "post",
        url="/api/users",
        data={"name": "Nikola Jokic", "job": "MVP"}
    )

    reqres.verify_code(response, 201)
    reqres.verify_response_json(response, 'name', 'Nikola Jokic')
    reqres.verify_response_json(response, 'job', 'MVP')
    reqres.verify_response_date_parameter(response, 'createdAt')


@allure.title('Verify error for not well-formed json for Create User')
@allure.feature('Single User')
@allure.story('Post Single User')
@allure.severity(Severity.NORMAL)
def test_create_new_user_non_well_formed_json():
    response = helper.api_request(
        "post",
        url="/api/users",
        headers={'Content-Type': 'application/json'},
        data='{\"name\" \"Michael Jordan\", \"job\": \"Nike\"}'
    )

    reqres.verify_code(response, 400)
    reqres.verify_response_text(response, 'Bad Request')


@allure.title('Verify Deletion of a User')
@allure.feature('Single User')
@allure.story('Delete Single User')
@allure.severity(Severity.CRITICAL)
def test_delete_user():
    id = 2

    response = helper.api_request("delete", url=f"/api/users/{id}")

    reqres.verify_code(response, 204)


@allure.title('Verify response schema for Patching of a User')
@allure.feature('Single User')
@allure.story('Patch Single User')
@allure.severity(Severity.CRITICAL)
def test_patch_user_response_schema():
    id = 5

    response = helper.api_request(
        "patch",
        url=f"/api/users/{id}",
        data={"name": "morpheus", "job": "unemployed"}
    )

    reqres.verify_code(response, 200)
    reqres.verify_schema(response, 'patch_user.json')


@allure.title('Verify Patching of a User')
@allure.feature('Single User')
@allure.story('Patch Single User')
@allure.severity(Severity.CRITICAL)
def test_patch_user_data():
    id = 5

    response = helper.api_request(
        "patch",
        url=f"/api/users/{id}",
        data={"name": "morpheus", "job": "unemployed"}
    )

    reqres.verify_code(response, 200)
    reqres.verify_response_json(response, 'name', 'morpheus')
    reqres.verify_response_json(response, 'job', 'unemployed')
    reqres.verify_response_date_parameter(response, 'updatedAt')


@allure.title('Verify error for not well-formed json for Patch User')
@allure.feature('Single User')
@allure.story('Patch Single User')
@allure.severity(Severity.NORMAL)
def test_patch_user_data_non_well_formed_json():
    id = 2

    response = helper.api_request(
        "patch",
        url=f"/api/users/{id}",
        headers={'Content-Type': 'application/json'},
        data="{\"name\": \"morpheus, \"job\": \"leader\"}"
    )

    reqres.verify_code(response, 400)
    reqres.verify_response_text(response, 'Bad Request')
