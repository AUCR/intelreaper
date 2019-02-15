"""Get config information or set defaults."""
# coding=utf-8
import os
from intelreaper.secrets.vault import get_config_from_vault
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):
    """Set environment variables based on config."""
    VAULT_URL = os.environ.get('VAULT_URL')
    VAULT_TOKEN = os.environ.get('VAULT_TOKEN')
    VAULT_SE = os.environ.get('VAULT_SE')
    VAULT_NAME = os.environ.get('VAULT_NAME')

    CONFIG_DATA = get_config_from_vault(VAULT_URL, VAULT_TOKEN, VAULT_SE, VAULT_NAME)

    def __repr__(self):
        """Return Config Data."""
        return '<Config {}>'.format(self.CONFIG_DATA)
