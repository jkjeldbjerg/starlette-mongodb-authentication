from pymongo.database import Database
from starlette.requests import Request
from starlette.templating import Jinja2Templates

from singletons.resources import Resources


class Views:
    """ Base init for a grouping of views
        Provide a link to the folder of relevant templates and a hook to the MongoDB database to be used

        This means that each view can be put into its own folder and run with separate database instances
        which can be useful when segregating user data from admin data

    """

    def __init__(self):
        """ init with template directory and database link """
        self.templates: Jinja2Templates = Resources().templates
        self.database: Database = Resources().db_data

    def add_message(self, request: Request, message: str, severity: str = 'info'):  # noqa
        """ add a message to the user in session

            Inspiration from starlette-core messages.
        """
        if 'messages' not in request.session:
            request.session['messages']: [dict] = []
        request.session['messages'].append({'message': message, 'severity': severity})