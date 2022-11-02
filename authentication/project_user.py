"""
    Project user is the implementation of a user with some parameters included.

"""

import base64
import hashlib
import hmac
import logging
import os
import re
from datetime import datetime

from pymongo.results import InsertOneResult
from starlette.authentication import BaseUser, UnauthenticatedUser
from bson import ObjectId

from singletons.resources import Resources


def generate_set(d: dict, t: str) -> set:
    """ generate a set of values from a string with space as delimiter """
    s = d[t] if t in d and d[t] is not None else ''
    result: set = set()
    if len(s) != 0:
        for item in s.split(' '):
            if item == '':
                continue
            result.add(item)
    return result


class ProjectUser(BaseUser):
    """ The project user object
        Suggested fields:
            usr: str: username
            pwd: str: hashed password (see ProjectUser.encode_password below, base64 encoded salt + password)
            name: str: real name
            scope: str: space separated list of scopes
            org: str: space separated list of organisations (for future SSO or for custom data views per org)
            created: datetime: datetime of creation
            password_age: datetime: datetime of current password creation
            updated: datetime: datetime of last change
            validated: datetime: datetime of validation or None
            locked: bool: if account is locked
            ... MongoDB lets you add more fields, if required
    """

    @staticmethod
    def find(_id: str):
        """ Find by _id in database. Only used by authenticate backend to load user from database """
        result: dict = Resources().db_admin.get_collection('users').find_one({'_id': ObjectId(_id)})
        if result is not None:
            return ProjectUser(result)

    @staticmethod
    def load(usr: str, pwd: str):
        """ load user from database if password is correct. Maybe use in basic authentication when implemented """
        result: dict = Resources().db_admin.get_collection('users').find_one({'usr': usr})
        if result is not None and 'pwd' in result and ProjectUser.check_password(pwd, result['pwd']):
            result['_id'] = str(result['_id'])
            return ProjectUser(result)

    @staticmethod
    def create(usr: str, pwd: str, name: str, scope: str, org: str = None):
        """ create from input variables. Used to create new user from view """
        if re.fullmatch(r"^[^@\s]+@[^.@\s]*\.[^\s]*$", usr) is None:
            logging.info(f"{usr} is not valid as an e-mail address: name={name}")
            raise ValueError(f"{usr} is not a valid e-mail address for {name}")

        info: dict = {
            'usr': usr,
            'pwd': ProjectUser.encode_password(pwd),
            'name': name,
            'scope': scope,
            'org': org,
            'created': datetime.now(),
            'password_age': datetime.now(),
            'updated': datetime.now(),
            'validated': None,
            'locked': False
        }
        return ProjectUser(info)

    def __init__(self, info):
        """ Should not be called directly, use factory methods above"""
        self.info: dict = info
        # building list of scopes for easy access
        self._scopes: set = generate_set(self.info, 'scope')
        # building list of organisations (org) for easy access
        self._org: set = generate_set(self.info, 'org')

    def _store(self):
        """ used for adding to db or updating existing one """
        self.info['scope'] = ' '.join(self._scopes)
        self.info['accessed'] = datetime.now()
        if '_id' not in self.info:
            ident: InsertOneResult = Resources().db_admin.get_collection('users').insert_one(self.info)
            self.info['_id'] = str(ident.inserted_id)
        else:
            Resources().db_admin.update_one({'_id': ObjectId(self.info['_id'])})

    def _refresh(self):
        """ refresh data from database """
        result: dict = Resources().db_admin.get_collection('users').find_one({'_id': ObjectId(self.info['_id'])})
        if result is None:
            logging.error("Could not refresh item %s, %s", self.info['usr'], self.info['_id'])
            raise ValueError(f"Could not refresh data item {self.info['usr']} from database")
        self._scopes = generate_set(result, 'scope')
        self._org = generate_set(result, 'org')
        self.info = result


    @property
    def display_name(self) -> str:
        """ display user's name (usr) """
        return self.info.get('usr', '')

    @property
    def identity(self) -> str:
        """ display name """
        return self.info.get('name', self.display_name)

    @property
    def is_authenticated(self) -> bool:
        """ is a user authenticated """
        if self.info['locked']:
            logging.info(f"User {self.display_name} ({self.identity}) is locked and tried to login")
        return not self.info['locked']

    @property
    def validated(self) -> bool:
        """ has the user validated his/her email or not """
        v = self.info.get('validated', False)
        return False if v is None else v

    def validate(self):
        """ the user validated her/his email """
        self.info['validated'] = datetime.now()
        self._store()

    def is_locked(self) -> bool:
        """ is the account locked. Default is False, i.e. not locked """
        return self.info.get('locked', False)

    @property
    def scopes(self) -> list:
        """ return the list of scopes
            note the internal representation of scopes is a Python set
        """
        return list(self._scopes)

    def add_scope(self, scope: str):
        """ add scope to set of scopes """
        self._scopes.add(str(scope))
        self._store()

    def remove_scope(self, scope: str):
        """ delete scope from set of scopes """
        self.scopes.remove(str(scope))

    def change_password(self, new_pwd: str):
        """ change password. Check for password quality before storing """
        self.info['pwd'] = ProjectUser.encode_password(new_pwd)
        self.info["password_age"] = datetime.now()
        self.info['updated'] = datetime.now()
        self._store()

    # password checking section ->
    # inspiration from this Stackoverflow: authentication - Salt and hash a password in Python - Stack Overflow
    # https://stackoverflow.com/questions/9594125/salt-and-hash-a-password-in-python/

    ALGORITHM: str = 'sha256'  # keep this
    ITERATIONS: int = 200000  # more iterations, longer processing time, pbkdf2 should be at least 100000 (10**5)
    SALT_LEN: int = 16  # length of salt

    @staticmethod
    def encode_password(password: str) -> str:
        """ encode a password with selected algorithm, length of salt and number of iterations as string """
        salt = os.urandom(ProjectUser.SALT_LEN)
        return base64.b64encode(salt + hashlib.pbkdf2_hmac(ProjectUser.ALGORITHM, password.encode(),
                                                           salt, ProjectUser.ITERATIONS)).decode('utf-8')

    @staticmethod
    def check_password(password: str, coded: str) -> bool:
        """ test if a password matches a previously encoded password with embedded salt """
        hashing = base64.b64decode(coded.encode('utf-8'))
        return hmac.compare_digest(
            hashing[ProjectUser.SALT_LEN:],
            hashlib.pbkdf2_hmac(ProjectUser.ALGORITHM, password.encode(),
                                hashing[:ProjectUser.SALT_LEN], ProjectUser.ITERATIONS)
        )

    # static checks on password

    PASSWORD_MIN_LEN: int = 8

    @staticmethod
    def password_quality(password: str) -> dict:
        """ return quality of password with explanation """
        result: dict = {  # noqa - silence complaint about dict init...
            'short': len(password) < ProjectUser.PASSWORD_MIN_LEN,
            # long: not checked -> can a password be too long?
            'only_letters': password.isalnum(),
            'only_lower': password.lower() == password,
            'only_upper': password.upper() == password,
            'only_digits': password.isdigit(),
            'only_symbols': re.search(r"^\W*$", password) is None,
            'no_letters': re.search(r"\w*", password) is None,
            'no_upper': not any([i.isupper() for i in password]),
            'no_lower': not any([i.islower() for i in password]),
            'no_digits': re.search(r"\d", password) is None,
            'no_symbols': re.search(r"\W", password) is None
        }

        # added for convenience:
        # quality measure: number of parameters measured - number not passed
        result['quality'] = {
            'quality': len(result) - len([i for i in result if i]),
            'max': len(result)
        }
        result['only'] = any([value for key, value in result.items() if 'only_' in key[:5]])
        result['no'] = any([value for key, value in result.items() if 'no_' in key[:3]])
        result['ok'] = not (result['short'] or result['only'] or result['no'])
        result['length'] = len(password)

        return result


class ProjectUnauthenticatedUser(UnauthenticatedUser):
    """ Fixing a minor issue in the UnauthenticatedUser class that throws error when requesting identity """

    @property
    def identity(self):
        """ This is not implemented in the UnauthenticatedUser class. Return no identity = None """
        return None



# EOF
