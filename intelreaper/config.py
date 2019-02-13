"""Get config information or set defaults."""
# coding=utf-8
import os
import click
from intelreaper.secrets.vault import get_config_from_vault
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):
    """Set environment variables based on config."""
    VAULT_URL = os.environ.get('VAULT_URL') or click.pass_context("--vault_url") or click.prompt("Vault API URL")
    VAULT_TOKEN = os.environ.get('VAULT_TOKEN') or click.pass_context("--vault_token") or click.prompt("Vault API Token")
    VAULT_SE = os.environ.get('VAULT_SE') or click.pass_context("--vault_se") or click.prompt("Vault Secrets Engine")
    VAULT_NAME = os.environ.get('VAULT_NAME') or click.pass_context("--vault_name") or click.prompt('Vault Name')

    CONFIG_DATA = get_config_from_vault(VAULT_URL, VAULT_TOKEN, VAULT_SE, VAULT_NAME)

    def __repr__(self):
        """Return Config Data."""
        return '<Config {}>'.format(self.CONFIG_DATA)
