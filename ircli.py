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
            md5_hash = report_data["analysis"]["content"]["mainObject"]["hashes"]["md5"]
            for item in processed_json["incidents"]:
                incidents_dict = flatten_dictionary(item)
                incidents_dict["process_time"] = report_process_time
                incidents_dict["md5_hash"] = md5_hash
                if "events" in incidents_dict:
                    for event_items in incidents_dict["events"]:
                        event_dict = flatten_dictionary(event_items)
                        event_dict["md5_hash"] = md5_hash
                        event_dict["process_time"] = report_process_time
                        index_data_to_es("anyrunevents", payload=event_dict)
                    del incidents_dict["events"]
                index_data_to_es("anyrunincidents", payload=incidents_dict)
            del processed_json["incidents"]
            for item in processed_json["processes"]:
                processes_dict = flatten_dictionary(item)
                processes_dict["process_time"] = report_process_time
                processes_dict["md5_hash"] = md5_hash
                index_data_to_es("anyrunprocesses", payload=processes_dict)
            del processed_json["processes"]
            for item in processed_json["mitre"]:
                mitre_dict = flatten_dictionary(item)
                mitre_dict["process_time"] = report_process_time
                mitre_dict["md5_hash"] = md5_hash
                index_data_to_es("anyrunmitre", payload=mitre_dict)
            del processed_json["mitre"]
            processed_json["process_time"] = report_process_time
            processed_json["main"] = flatten_dictionary(report_data["analysis"]["content"]["mainObject"]["info"])
            processed_json["hashes"] = flatten_dictionary(report_data["analysis"]["content"]["mainObject"]["hashes"])
            processed_json["md5_hash"] = md5_hash
            del processed_json["report"]["analysis.content.mainObject.hashes"]
            del processed_json["report"]["analysis.content.mainObject.info"]
            if "pe" in processed_json["main"]:
                for pe_item in processed_json["main"]["pe"]:
                    pe_dict = flatten_dictionary_with_int(pe_item)
                    pe_dict["process_time"] = report_process_time
                    pe_dict["md5_hash"] = md5_hash
                    for value_item in processed_json["main"]["pe"]:
                        pe_dict[str(value_item["key"])] = str(value_item["value"])
                    del pe_dict["value"]
                    index_data_to_es("anyrunpe", payload=pe_dict)
                del processed_json["main"]["pe"]
            if "trid" in processed_json["main"]:
                for trid_item in processed_json["main"]["trid"]:
                    trid_dict = flatten_dictionary(trid_item)
                    trid_dict["process_time"] = report_process_time
                    trid_dict["md5_hash"] = md5_hash
                    index_data_to_es("anyruntrid", payload=trid_dict)
                del processed_json["main"]["trid"]
            index_data_to_es("anyrunreport", payload=processed_json)


if __name__ == '__main__':
    intel_reaper()
