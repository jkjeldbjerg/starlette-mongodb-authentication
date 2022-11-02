# DB and auth Starlette base project

Template for starting a new project with MongoDB Database and authentication enabled.

This template has been made to be fully functional. You do need, however, to set up the MongoDB
yourself, or have one available.

**The pages given here are not to be used in production!** They all contain data and links that are 
very bad for security!

## Using this repository

You will want to clone this repository and build your own application on top.

Details on how to run the application can be found in `documentation/running.md`.

## Cookie concern

Due to rules and regulations we need to state in our terms that we use technical cookies.

The cookie used is a session cookie encoding a unique identifier of the user. The cookie is not 
used for tracking purposes other than keeping a user logged in.

## Config 

Key is set by using `bcrypt.gensalt(32)` from `bcrypt` (install: `pip install py-bcrypt`).

Config is accessed through the singleton class 

`db_auth_singletons.resources.Resources(metaclass=metaclasses.singleton.Singleton)`

Easiest to import:

`from db_auth_singletons.resources import Resources`

Access to `Jinja2Templates` is through the `templates` property, databases are accessed 
through `db_data` (for data) and `db_admin` (for admin).
Other attributes can be accessed using `get(key, default = None)`.

## Pages

Initially these routes/pages

* `/` - home, no authentication required
* `/login` - login page, username and password 
* `/logout` - logout page
* `/authenticated` - page available when `authenticated`
* `/db/test` - page for showing connection to the data MongoDB database, requires scope `admin`
* `/auth/test` - page for showing connection to the admin MongoDB database, requires scope `admin`

## Database

The supported database is [MongoDB](https://www.mongodb.com/). It is a NoSQL database which means 
that it does not have a fixed schema for a table. 

Setting up a MongoDB database can be done by following 
the instructions 
[Install MongoDB Community Edition](https://www.mongodb.com/docs/manual/administration/install-community/) 

Javascript for setting up the databases. Assumption is that you are logged in to `mongosh` as 
an admin and that you substitute `project_data`, `project_admin`, `project_user` with 
appropriate values. Remember to save the password.

```javascript
// admin first
use project_admin
db.createCollection('users')
db.createCollection('authentication')
db.createCollection('scopes')

// data next  whatever you need to put here
use project_data
db.createCollection('some_data')
// ... 

// create the database user
use project_data
db.createUser({'user':'project_user','pwd': password(), 
    'roles': [{'role':'readWrite',db:'project_data'}, {'role':'readWrite',db:'project_data'}]})
```

Testing working on MongoDB 1.6.0

### Database collections

#### Admin collections

Tables required are:

* `users` - contains the list of users with fields: usr, pwd(hashed), name, scope (str of scopes)
* `scopes` - contains the list of authorised scopes. 

#### Data collections

This is where you add your own collections.


## Test flows

See the file `documentation/Auth_test_cases.md` for a list of cases

## License

This project is licensed under the terms of the MIT license, see `LICENSE`.

## Thank you

This project has taken a lot of inspiration from the 
[Starlette-Core project](Starlette Core
https://accent-starlette.github.io/starlette-core/). Thank you for the good work. Appreciated.