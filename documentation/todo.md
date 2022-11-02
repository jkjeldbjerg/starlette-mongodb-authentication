# TODO's

## Refactor

Move all the code into a folder to avoid cluttering up the workspace.

I am thinking in lines of 

```
project_root
|
+- /mongo_authentication
|  +- /templates         // authentication templates, must be replaceable by user supplied templates
|  +- /views             // classes for views
|  +- /authentication    // authentication middleware
|  +- /tests             // test cases / modules
|  +- /documentation     // documentation of system
|  +- /bootstrapping     // getting started on project with some sane values
|
+- /metaclasses          // generally useful
+- /singletons           // resources
|
+- /static               // where stylesheets, javascripts etc. go
+- /files                // private files
+- /templates            // regular templates; must be possible to supply own templates for auth
+- LICENSE               // MIT license file
+- README.md             // introduction and getting started
+- requirements.txt      // pip requirements
+- app.py                // main application runner
```

It would be neat to have a '/application' folder for the specific code, pages, etc. for running the 
application. Like:

```
project_root
 ...
|
+- /application          // application folder
   +- /views             
   +- /templates
   +- /static
   +- /files
```

Something to think about.

## Tests

Finalise list of test cases in `Auth_test_cases.md`.

Write automated tests.
* Some are done for testing features on login, logout, scopes
* Not getting server running in tests, maybe: 
* [Stackoverflow: how-to-start-a-uvicorn-fastapi-in-background-when-testing-with-pytest](https://stackoverflow.com/questions/57412825/how-to-start-a-uvicorn-fastapi-in-background-when-testing-with-pytest)

## CSRF

Implement CSRF for forms. Add hidden item in form with key and also have session store key encrypted.
Note: If more tabs are open then session "nonce" can be invalid when form is finally submitted. Because
something else is going on in another window.

[CSRF middleware](https://github.com/gnat/csrf-starlette-fastapi/blob/main/csrf_middleware.py)