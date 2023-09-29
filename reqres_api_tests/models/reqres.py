import jsonschema
import allure
from reqres_api_tests.utils import helper
from datetime import datetime


def verify_response_json_data(response, parameter, value):
    with allure.step(f'Verify response json contains "data" with "{parameter}" = {value}'):
        assert response.json()['data'][parameter] == value


def verify_response_json(response, parameter, value):
    with allure.step(f'Verify response json contains "{parameter}" = {value}'):
        assert response.json()[parameter] == value


def verify_code(response, code):
    with allure.step(f'Verify response code is {code}'):
        assert response.status_code == code


def verify_schema(response, file_name):
    with allure.step('Verify response schema'):
        schema = helper.response_schema(helper.path_dir('resources', 'schemas', file_name))
        jsonschema.validators.validate(instance=response.json(), schema=schema)


def verify_response_text(response, text):
    with allure.step(f'Verify response text/html contains <{text}>'):
        assert text in response.text


def verify_empty_response(response):
    with allure.step('Verify response has no data'):
        assert response.json() == {}


def verify_response_date_parameter(response, parameter):
    with allure.step(f'Verify "{parameter}" contains current date'):
        assert response.json()[parameter][:16] == datetime.utcnow().strftime("%Y-%m-%dT%H:%M")


def verify_avatar_as_referenced(image1, image2):
    with allure.step('Verify avatar corresponds to a reference'):
        assert helper.are_images_equal(image1, image2)


def verify_amount_users_shown(response, amount):
    with allure.step(f'Verify amount of users shown is {amount}'):
        assert len(response.json()['data']) == amount

def verify_correct_values_for_parameter(response, parameter, list):
    with allure.step(f'Verify presented {parameter}s are correct in response json'):
        assert list == [user[parameter] for user in response.json()['data']]