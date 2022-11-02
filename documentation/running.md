# Running the app

**¡For a production setup, read the bottom!**

If you not already have installed `venv` this is the time to do so. The following commands will
install it

```shell
python3 -m venv venv
```

After installation, you need to activate venv and install dependencies:

```shell
source venv/bin/activate
pip -r requirements.txt
```

You only need to do the `pip` the first time you activate. After the first time all is installed.

### Simple

```shell
python3 app
```

This will run the application as a `uvicorn` instance on [http://0.0.0.0:8260/](http://0.0.0.0:8260/).

See `app.py` line 75.

### Gunicorn

```shell
gunicorn -w 4 -k uvicorn.workers.UvicornH11Worker app:main
```

This will run the application under `gunicorn` with `uvicorn` workers on 
[http://localhost:8000](http://localhost:8000).

### Production

In a production setup you want to tweak the `config.json` to something like what is in the file:
`files/config_template_prod.json`:

```json
{
  "logging": "INFO",
  "debug": false,
    "mongo": { /* ... */ }
}
```

Logging is not required at DEBUG level, set to INFO instead.

You also do not want the Starlette debugger to show up for users in case something goes awry...


