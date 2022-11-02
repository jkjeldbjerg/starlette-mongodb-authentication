import logging
import sys

from authentication.project_user import ProjectUser
from singletons.resources import Resources


def main():
    logging.basicConfig(stream=sys.stdout,
                        format=f'%(asctime)s %(levelname)s: %(message)s',  # noqa
                        level=logging.DEBUG)
    # init resources
    Resources('../files/config.json', 'templates')

    docs = Resources().db_admin.get_collection('users').count_documents({})
    print("Documents", docs)

    Resources().db_admin.get_collection('users').delete_many({})

    print("Do normal user")
    pu: ProjectUser = ProjectUser.create('user@space.net', '1234', 'User 1', 'authenticated', '')
    print("Do admin user")
    adm: ProjectUser = ProjectUser.create('adm@nowhere.here', '1234', 'Adm 1', 'authenticated admin', '')

    docs = Resources().db_admin.get_collection('users').count_documents({})
    print("Documents", docs)

    one = Resources().db_admin.get_collection('users').find_one({'usr': 'user@space.net'})
    print(one)


if __name__ == '__main__':
    main()

# EOF
