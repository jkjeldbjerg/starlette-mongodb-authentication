import logging

from pymongo.database import Database
from starlette.authentication import requires
from starlette.requests import Request
from starlette.responses import RedirectResponse, JSONResponse

from authentication.project_user import ProjectUser
from singletons.resources import Resources
from views.views import Views


class AuthenticationViews(Views):
    """ Views concerning authenticating a user
        Will use a MongoDB (see Views.__init__) for credentials
    """

    def __init__(self):
        """ init as other views, but with the db_admin database as default """
        super().__init__()
        self.database: Database = Resources().db_admin

    async def login(self, request: Request):
        """ /login - login page

            Note: in the request.query_params there may be a next=<url> for sending user to the right place
            after. Add this to the login form to make do_login redirect
        """
        logging.debug("AuthenticationViews.login: started")
        return self.templates.TemplateResponse('auth/login.html', {'request': request})

    async def do_login(self, request: Request):
        """ POST /login - the logging-in logic """
        logging.debug("AuthenticationViews.do_login: started")
        # auto-logout if already logged in:
        request.session.clear()
        # get form data for login
        form_data = await request.form()
        usr = form_data.get('usr', None)
        pwd = form_data.get('pwd', None)

        # find user
        project_user = ProjectUser.load(usr, pwd)
        if project_user is None:
            if usr is not None:
                self.add_message(request, "Invalid username or password")
                return RedirectResponse(request.url_for('login'), status_code=303)
            return RedirectResponse(request.url_for('home'), status_code=303)
        else:
            request.session['user'] = str(project_user.info['_id'])
            self.add_message(request, f"Login successful. Welcome {project_user.identity}!")
            if 'next' in request.query_params and request.query_params['next'] != '':
                return RedirectResponse(request.query_params['next'], status_code=303)
            return RedirectResponse(request.url_for('authenticated'), status_code=303)

    @requires('authenticated', redirect='login')
    async def logout(self, request: Request):
        """ /logout - logout from system """
        logging.debug("AuthenticationViews.logout: started")
        request.session.clear()
        self.add_message(request, "Logout successful. See you soon!")
        return RedirectResponse(request.url_for('home'), status_code=303)

    @requires('admin', redirect='login')
    async def create_user(self, request: Request):
        """ /admin/user/create - create a new user """
        logging.debug("AuthenticationViews.create_user: started")
        return self.templates.TemplateResponse('create_user.html', {'request': request})

    @requires('admin', redirect='login')
    async def do_create_user(self, request: Request):
        raise NotImplementedError('No implementation of user creation')

    # utility API methods

    async def pwd_quality(self, request):  # noqa -- it may be static, maybe not
        """ Return the test of the password quality. Used in create user views """
        form = await request.form()
        if 'pwd' not in form:
            return JSONResponse({}, status_code=200)
        quality = ProjectUser.password_quality(form.get('pwd'))
        return JSONResponse({
            'quality': quality
        }, status_code=200)

    # test methods for checking access to database etc.

    @requires('admin', redirect='login')
    async def test_db(self, request: Request):
        """ can we connect to admin database and get a result from it """
        logging.debug("AuthenticationViews.test_db: started")
        d = self.database['authentication'].find_one()
        return self.templates.TemplateResponse('auth/test_db.html', {
            'request': request,
            'data': "Admin: Data found" if d is not None and len(d) > 0 else 'No data returned'
        })