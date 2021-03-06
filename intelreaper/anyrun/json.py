import udatetime
from dataparserlib.dictionary import flatten_dictionary, flatten_dictionary_with_int
from intelreaper.reporting.es import index_data_to_es


def index_file_json_report(report_data):
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
                index_data_to_es("arevents", payload=event_dict)
            del incidents_dict["events"]
        index_data_to_es("arincidents", payload=incidents_dict)
    del processed_json["incidents"]
    for item in processed_json["processes"]:
        processes_dict = flatten_dictionary(item)
        processes_dict["process_time"] = report_process_time
        processes_dict["md5_hash"] = md5_hash
        index_data_to_es("arprocesses", payload=processes_dict)
    del processed_json["processes"]
    if "mitre" in processed_json:
        for item in processed_json["mitre"]:
            mitre_dict = flatten_dictionary(item)
            mitre_dict["process_time"] = report_process_time
            mitre_dict["md5_hash"] = md5_hash
            index_data_to_es("armitre", payload=mitre_dict)
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
            index_data_to_es("arpe", payload=pe_dict)
        del processed_json["main"]["pe"]
    if "trid" in processed_json["main"]:
        for trid_item in processed_json["main"]["trid"]:
            trid_dict = flatten_dictionary(trid_item)
            trid_dict["process_time"] = report_process_time
            trid_dict["md5_hash"] = md5_hash
            index_data_to_es("artrid", payload=trid_dict)
        del processed_json["main"]["trid"]
    index_data_to_es("arreport", payload=processed_json)
