""" Project views

    Should be split into class files for a larger site. Here we keep them in one place to have an easy overview
    while trying out the services
"""

import logging

from starlette.authentication import requires
from starlette.requests import Request

from views.views import Views


class BasicViews(Views):
    """ Basic simple views """

    async def home(self, request: Request):
        """ / view in application """
        logging.debug("BasicViews.home: started")
        return self.templates.TemplateResponse('home.html', {
            'request': request
        })

    @requires('authenticated', redirect='login')
    async def authenticated(self, request: Request):
        """ /authenticated view in application requiring user to be logged in """
        logging.debug("BasicViews.authenticated: started")
        return self.templates.TemplateResponse('authenticated.html', {'request': request})

    @requires('admin', redirect='login')
    async def test_db(self, request: Request):
        """ /test_db view to see if data is returned from database """
        logging.debug("BasicViews.test_db: started")
        d = self.database.get_collection('company').find_one({})
        return self.templates.TemplateResponse('auth/test_db.html', {
            'request': request,
            'data': "Data: Data found" if d is not None and len(d) > 0 else 'No data returned'
        })

# EOF
