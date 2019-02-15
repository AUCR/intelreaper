import ujson
import click
import sys
import time
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from intelreaper.anyrun.json import index_file_json_report
from yaml_info.yamlinfo import YamlInfo

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')


class Handler(FileSystemEventHandler):
    @staticmethod
    def on_any_event(event):
        if event.is_directory:
            return None
        elif event.event_type == 'created':
            with open(str(event.src_path), 'r') as input_file:
                report_data = ujson.load(input_file)
            index_file_json_report(report_data)


@click.group()
@click.option('--debug/--no-debug')
def cli(debug):
    click.echo('Debug mode is %s' % ('on' if debug else 'off'))


def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo(YamlInfo("projectinfo.yml", "projectinfo", "LICENSE"))
    ctx.exit()


@click.command()
@click.option("--plugin", "-p", help="Select a plugin to use.")
@click.option("--input_file", type=click.File('rb'), help="The Input File.")
@click.option("--input_source", help="The Input File Source.")
@click.option("--report", help="The desired report location.")
@click.option('--version', is_flag=True, callback=print_version, expose_value=False, is_eager=True)
@click.option("--volume", help="The desired volume to monitor.")
def intel_reaper(plugin, input_file, report, input_source, volume):
    if plugin == "json":
        if input_file:
            report_data = ujson.load(input_file)
            if report == "es":
                if input_source == "any.run":
                    index_file_json_report(report_data)
        if volume:
            path = volume
            event_handler = Handler()
            observer = Observer()
            observer.schedule(event_handler, path, recursive=True)
            observer.start()
            try:
                while True:
                    time.sleep(5)
            except KeyboardInterrupt:
                observer.stop()
            observer.join()


