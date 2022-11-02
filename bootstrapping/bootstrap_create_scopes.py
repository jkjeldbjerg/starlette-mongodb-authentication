""" This will create the initial set of scopes in collection `scopes` """

import logging
import sys

from pymongo.collection import Collection
from pymongo.results import InsertOneResult

from singletons.resources import Resources


def main():
    """ create a minimal set of scopes """
    logging.basicConfig(stream=sys.stdout,
                        format=f'%(asctime)s %(levelname)s: %(message)s',  # noqa
                        level=logging.DEBUG)
    # init resources
    Resources('../files/config.json', 'templates')

    scope_collection: Collection = Resources().db_admin.get_collection('scopes')

    scopes = [
        {'scope': 'authenticated', 'name': 'Authenticated', 'description': 'Set for all authenticated users'},
        {'scope': 'admin', 'name': 'Administrator', 'description': 'Systems administrator'},
    ]

    for scope in scopes:
        """ avoid duplication by upserting """
        scope_collection.find_one_and_update({'scope': scope['scope']}, {'$set': scope}, upsert=True)


if __name__ == '__main__':
    main()

# EOF
