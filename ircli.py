"""The Intelreaper python command line interface."""
# coding=utf-8
import os
import ujson
import click
import udatetime
from dataparserlib.dictionary import flatten_dictionary, flatten_dictionary_with_int
from intelreaper.config import Config
from intelreaper.reporting.es import index_data_to_es

VAULT_URL = os.environ.get('VAULT_URL') or click.get_current_context("--vault_url")
VAULT_TOKEN = os.environ.get('VAULT_TOKEN') or click.get_current_context("--vault_token")
VAULT_SE = os.environ.get('VAULT_SE') or click.get_current_context("--vault_se")
VAULT_NAME = os.environ.get('VAULT_NAME') or click.get_current_context("--vault_name")
ELASTICSEARCH_URL = None
if "ELASTICSEARCH_URL" in Config.CONFIG_DATA:
    ELASTICSEARCH_URL = Config.CONFIG_DATA["ELASTICSEARCH_URL"]


@click.command()
@click.option("--plugin", help="Select a plugin to use.")
@click.option("--vault_token", help="The Vault API Token.")
@click.option("--vault_url",  help="The vault API URL.")
@click.option("--vault_se", help="The Vault Secret Engine.")
@click.option("--vault_name", help="The Vault Secret Name.")
@click.option("--input_file", help="The Input File.")
@click.option("--report", help="The desired report location.")
def intel_reaper(plugin, vault_token, vault_url, vault_se, vault_name, input_file, report):
    if plugin == "json":
        with open(input_file, 'r') as input_data:
            raw_file = input_data.read()
            report_data = ujson.loads(raw_file)
        if report == "es":
            report_process_time = udatetime.now_to_string()
            processed_json = flatten_dictionary(report_data)
            for item in processed_json["incidents"]:
                incidents_dict = flatten_dictionary_with_int(item)
                incidents_dict["process_time"] = report_process_time
                index_data_to_es("anyrunincidents", payload=incidents_dict)
            del processed_json["incidents"]
            processed_json["process_time"] = report_process_time
            index_data_to_es("anyruntest", payload=processed_json)


if __name__ == '__main__':
    intel_reaper()
