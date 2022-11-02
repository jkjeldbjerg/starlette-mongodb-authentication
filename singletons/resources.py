""" Resources contain all the common dependencies required by various modules

    SOMEDAY-MAYBE: Might someday create a real dependency injection mechanism
"""

import pymongo
from pymongo.database import Database
from starlette.templating import Jinja2Templates
import logging
import json
import pathlib

from typing import Any

from metaclasses.singleton import Singleton


class Resources(metaclass=Singleton):
    """ Singleton resource class """

    def __init__(self, config_file: str = None, template_dir: str = None):
        """ setup the singleton class """
        logging.debug("Resources.__init__: started")
        if config_file is None or template_dir is None:
            logging.error("Resources.__init__: did not get required parameters. Did you miss first instantiation?")
            raise KeyError("Did not get required parameters")
        try:
            self.cfg: dict = json.loads(pathlib.Path(config_file).read_text())
        except FileNotFoundError as e:
            logging.fatal("Could not open config file %s", config_file, exc_info=True)
            raise e

        # Jinja2 templates
        self.templates: Jinja2Templates = Jinja2Templates(directory=template_dir)

        # setup mongoDB connection
        mongo: dict = self.cfg['mongo']
        connect: str = f"mongodb://{mongo['usr']}:{mongo['pwd']}@{mongo['url']}/{mongo['db']}"
        self.db_client: pymongo.MongoClient = pymongo.MongoClient(connect)
        self.db_data: Database = self.db_client.get_database(mongo['db'])
        if 'admin' not in mongo or mongo['admin'] is None or mongo['admin'] == '':
            self.db_admin = self.db_data
        else:
            self.db_admin: Database = self.db_client.get_database(mongo['admin'])

    def get(self, key: str, default: Any = None):
        """ get a config attribute with default option """
        return self.cfg.get(key, default)


# EOF
