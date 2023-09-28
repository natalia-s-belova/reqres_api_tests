import os
import json
import tests
import allure
import requests
from requests import sessions
from curlify import to_curl
from allure_commons.types import AttachmentType


def path_dir(*file_path):
    return os.path.abspath(os.path.join(os.path.dirname(tests.__file__), *file_path))


def response_schema(file_path):
    with open(file_path, encoding='utf-8') as file:
        schema = json.loads(file.read())
    return schema


def api_request(method, url, **kwargs):
    base_url = "https://reqres.in"
    new_url = base_url + url
    with allure.step(f"{method.upper()} {new_url}"):
        with sessions.Session() as session:
            response = session.request(method=method, url=new_url, **kwargs)
            message = to_curl(response.request)
            allure.attach(body=message.encode("utf-8"), name="Curl", attachment_type=AttachmentType.TEXT,
                          extension='txt')
            if not response.content:
                allure.attach(body='empty response', name='Empty Response', attachment_type=AttachmentType.TEXT,
                              extension='txt')
            elif 'text/html' in response.headers['Content-Type']:
                allure.attach(body=response.content, name='Text/HTML Response', attachment_type=AttachmentType.TEXT,
                              extension='txt')
            elif 'application/json' in response.headers['Content-Type']:
                allure.attach(body=json.dumps(response.json(), indent=4).encode("utf-8"), name="Response Json",
                              attachment_type=AttachmentType.JSON, extension='json')
    return response


def are_images_equal(image1, image2):
    from PIL import Image, ImageChops
    return not ImageChops.difference(Image.open(image1), Image.open(image2)).getbbox()


def download_file_by_url_as(url, new_file):
    response = requests.get(url)
    with open(new_file, 'wb') as file:
        file.write(response.content)
