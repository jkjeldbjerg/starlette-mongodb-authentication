import logging
import sys
from typing import Optional, Union

import uvicorn as uvicorn
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.routing import Route, Mount
from starlette.staticfiles import StaticFiles

from views.basic_views import BasicViews
from views.authentication_views import AuthenticationViews
from authentication.authentication import BasicAuthBackend
from middleware.session_middleware import ProjectSessionMiddleware
from singletons.resources import Resources


def main(local: bool = False) -> Union[int, Starlette]:
    """ main execution function """
    # Setup logging
    logging.basicConfig(stream=sys.stdout,
                        format=f'%(asctime)s %(levelname)s: %(message)s',  # noqa
                        level=logging.DEBUG)

    # Setup config
    # See files/config_template.json for format
    try:
        Resources('files/config.json', 'templates')  # initialise singleton first use
    except FileNotFoundError:
        return 1
    logging.getLogger().setLevel(Resources().get('logging', 'DEBUG'))

    # setup page class
    pages: BasicViews = BasicViews()
    auth_pages: AuthenticationViews = AuthenticationViews()

    # setup Starlette app
    debug = Resources().get('debug', False)
    app = Starlette(debug=debug,
                    routes=[
                        # base pages
                        Route('/', pages.home, name='home'),
                        Route('/authenticated', pages.authenticated, name='authenticated'),

                        # base pages: test DB connectivity
                        Route('/db/test', pages.test_db, name='test_db'),

                        # auth pages
                        Route('/login', auth_pages.login, name='login'),
                        Route('/login', auth_pages.do_login, name='do_login', methods=['POST']),
                        Route('/logout', auth_pages.logout, name='logout'),
                        Route('/pwd_quality', auth_pages.pwd_quality, name='pwd_quality', methods=['GET']),

                        # auth pages: test DB connectivity
                        Route('/auth/test', auth_pages.test_db, name='auth_db'),

                        Mount('/admin', routes=[
                            Route('/user/create', auth_pages.create_user, name='create_user'),
                            Route('/user', auth_pages.do_create_user, name='do_create_user', methods=['POST'])
                        ]),


                        # Mount static file directory last:
                        Mount("/static", app=StaticFiles(directory="static"), name="static"),
                    ],
                    middleware=[
                        Middleware(AuthenticationMiddleware, backend=BasicAuthBackend(allow_basic_auth=True))
                    ])
    app.add_middleware(SessionMiddleware, secret_key=ProjectSessionMiddleware(app, Resources().get('key')))

    # run this as the main task if local is set. Default is not to run
    if local:
        uvicorn.run(app, host='0.0.0.0', port=8260)  #
        Resources().db_client.close()
    else:
        return app
    # no return when successful - the Optional bit


if __name__ == '__main__':
    """ Run main """
    code: int = main(local=True)
    if type(code) is Starlette:
        pass
    elif code is not None:
        exit(code)

# EOF
