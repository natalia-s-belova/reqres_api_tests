import jsonschema
from reqres_api_tests.utils import helper
import os
import datetime


def test_users_list_response_schema():
    schema = helper.response_schema(helper.path_dir('resources', 'schemas', 'get_users_list.json'))

    response = helper.api_request("get", url="/api/users")

    assert response.status_code == 200
    jsonschema.validators.validate(instance=response.json(), schema=schema)


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

    emails_in_json = [user['email'] for user in response.json()['data']]

    assert response.status_code == 200
    assert response.json()['total'] == per_page
    assert len(emails_in_json) == per_page
    assert registered_emails == emails_in_json


def test_users_list_names_are_correct_and_pagination_applied():
    per_page = 4
    page_number = 3
    users_shown = ['Tobias Funke',
                   'Byron Fields',
                   'George Edwards',
                   'Rachel Howell']

    response = helper.api_request("get", url="/api/users", params={"per_page": per_page, "page": page_number})

    users_in_response = [f"{user['first_name']} {user['last_name']}" for user in response.json()['data']]

    assert response.status_code == 200
    assert response.json()['total'] == 12
    assert len(users_in_response) == per_page
    assert users_shown == users_in_response


def test_users_list_when_per_page_amount_more_than_existing_users():
    per_page = 20

    response = helper.api_request("get", url="/api/users", params={"per_page": per_page})

    assert response.status_code == 200
    assert response.json()['per_page'] == per_page
    assert len(response.json()['data']) == 12


def test_user_single_response_schema():
    id = 7
    schema = helper.response_schema(helper.path_dir('resources', 'schemas', 'get_single_user.json'))

    response = helper.api_request("get", url=f"/api/users/{id}")

    assert response.status_code == 200
    jsonschema.validators.validate(instance=response.json(), schema=schema)


def test_single_existing_user_data():
    id = 8

    response = helper.api_request("get", url=f"/api/users/{id}")

    assert response.status_code == 200
    assert response.json()['data']['id'] == id
    assert response.json()['data']['email'] == 'lindsay.ferguson@reqres.in'
    assert response.json()['data']['first_name'] == 'Lindsay'
    assert response.json()['data']['last_name'] == 'Ferguson'
    assert response.json()['data']['avatar'] == 'https://reqres.in/img/faces/8-image.jpg'


def test_single_user_avatar():
    id = 7

    response = helper.api_request("get", url=f"/api/users/{id}")

    reference = helper.path_dir('resources', 'images', f'{id}.jpeg')
    actual = helper.path_dir('resources', 'images', 'downloaded.jpeg')
    helper.download_file_by_url_as(response.json()['data']['avatar'], actual)

    assert helper.are_images_equal(actual, reference)

    os.remove(actual)


def test_single_non_existing_user():
    id = 23

    response = helper.api_request("get", url=f"/api/users/{id}")

    assert response.status_code == 404
    assert response.json() == {}


def test_create_user_response_schema():
    schema = helper.response_schema(helper.path_dir('resources', 'schemas', 'post_user.json'))

    response = helper.api_request(
        "post",
        url="/api/users",
        data={"name": "morpheus", "job": "leader"}
    )

    assert response.status_code == 201
    jsonschema.validators.validate(instance=response.json(), schema=schema)


def test_create_new_user():
    response = helper.api_request(
        "post",
        url="/api/users",
        data={"name": "Nikola Jokic", "job": "MVP"}
    )

    assert response.status_code == 201
    assert response.json()['name'] == 'Nikola Jokic'
    assert response.json()['job'] == 'MVP'
    assert response.json()['createdAt'][:16] == datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M")


def test_create_new_user_non_well_formed_json():
    response = helper.api_request(
        "post",
        url="/api/users",
        headers={'Content-Type': 'application/json'},
        data='{\"name\" \"Michael Jordan\", \"job\": \"Nike\"}'
    )

    assert response.status_code == 400
    assert 'Bad Request' in response.text


def test_delete_user():
    id = 2

    response_del = helper.api_request("delete", url=f"/api/users/{id}")

    assert response_del.status_code == 204


def test_patch_user_response_schema():
    id = 5
    schema = helper.response_schema(helper.path_dir('resources', 'schemas', 'patch_user.json'))

    response = helper.api_request(
        "patch",
        url=f"/api/users/{id}",
        data={"name": "morpheus", "job": "unemployed"}
    )

    assert response.status_code == 200
    jsonschema.validators.validate(instance=response.json(), schema=schema)


def test_patch_user_data():
    id = 5

    response = helper.api_request(
        "patch",
        url=f"/api/users/{id}",
        data={"name": "morpheus", "job": "unemployed"}
    )

    assert response.status_code == 200
    assert response.json()['name'] == 'morpheus'
    assert response.json()['job'] == 'unemployed'
    assert response.json()['updatedAt'][:16] == datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M")


def test_patch_user_data_non_well_formed_json():
    id = 2

    response = helper.api_request(
        "patch",
        url=f"/api/users/{id}",
        headers={'Content-Type': 'application/json'},
        data="{\"name\": \"morpheus, \"job\": \"leader\"}"
    )

    assert response.status_code == 400
    assert 'Bad Request' in response.text
