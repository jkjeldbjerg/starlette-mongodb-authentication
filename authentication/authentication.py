import logging

from starlette.authentication import AuthenticationBackend, AuthCredentials
from starlette.requests import HTTPConnection

from authentication.project_user import ProjectUser, ProjectUnauthenticatedUser
from singletons.resources import Resources


class BasicAuthBackend(AuthenticationBackend):
    """ Authentication backend """

    def __init__(self, allow_bearer_auth: bool = False, allow_basic_auth: bool = False):
        """ set access to database, allow authentication by either basic or bearer or both """
        logging.debug("BasicAuthBackend.__init__: started")
        super().__init__()
        self.db_admin = Resources().db_admin
        if not (allow_basic_auth or allow_bearer_auth):
            raise ValueError("Allow at least one of basic or bearer authentication")
        self.allow_token_auth: bool = allow_bearer_auth
        self.allow_basic_auth: bool = allow_basic_auth

    async def authenticate(self, conn: HTTPConnection):
        """ Authenticate a user in the request context
            Allowed authentication methods are:
            - session (default)
        """

        logging.debug('BasicAuthBackend.authenticate: started')

        if "user" in conn.session:
            logging.debug('BasicAuthBackend.authenticate: session authorization')
            _id = conn.session.get('user')
            pu = ProjectUser.find(_id)
            logging.debug(f"  - user in session: {_id}, usr={pu.info['usr']}")
            if pu.is_authenticated:
                return AuthCredentials(list(pu.scopes)), pu

        elif "Authorization" in conn.headers:
            logging.debug("BasicAuthBackend.authenticate: basic authorization / bearer authentication")
            auth = conn.headers["Authorization"]
            scheme, credentials = auth.split()
            if scheme.lower() == 'bearer' and self.allow_token_auth:
                logging.debug('  - login with bearer token')
                raise NotImplementedError('Authentication with bearer token not supported')
            elif scheme.lower() == 'basic' and self.allow_basic_auth:
                logging.debug('  - login with basic authentication')
                raise NotImplementedError('Authentication with basic auth not supported')
            else:
                pass
        else:
            return AuthCredentials(['unauthenticated']), ProjectUnauthenticatedUser()
            # THIS IS OLD CODE FOR INSPIRATION WHEN DOING BASIC AUTH
            # try:
            #     if scheme.lower() != 'bearer' and self.allow_token_auth:
            #         raise NotImplementedError('authenticate for token')
            #     elif scheme.lower() == 'basic' and self.allow_basic_auth:
            #         decoded = base64.b64decode(credentials).decode("ascii")
            #         raise NotImplementedError('authenticate for basic')
            #     else:
            #         logging.debug("BasicAuthBackend.authenticate: return because no credentials")
            # except (ValueError, UnicodeDecodeError, binascii.Error) as exc:
            #     raise AuthenticationError('Invalid basic auth credentials')
            #
            # username, _, password = decoded.partition(":")
            # logging.debug("BasicAuthBackend.authenticate: ready to supply user")
            # return AuthCredentials(["authenticated"]), SimpleUser(username)


# EOF
