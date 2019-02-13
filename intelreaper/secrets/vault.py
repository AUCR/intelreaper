"""Intelreaper Vault library."""
# coding=utf-8
import ujson
import requests


def get_config_from_vault(api_url, api_key, secrets_engine_name, secrets_name):
    """Initialize intelreaper config from Vault SE.
    @param api_url: Vault URL.
    @param api_key: Vault API token.
    @param secrets_engine_name: Vault Secret Engine.
    @param secrets_name: Vault Secret Name.
    """
    headers = {'Authorization': 'Bearer ' + str(api_key)}
    response = requests.get('{}/v1/{}/data/{}'.format(api_url, secrets_engine_name, secrets_name), headers=headers)
    response_json = ujson.loads(response.text)
    valid_data = {}
    if 200 == response.status_code:
        valid_data = response_json["data"]["data"]
    elif 403 == response.status_code:
        return valid_data
    return valid_data
