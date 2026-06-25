# Bag Amsterdam Api

This is a proxy service to connect to the RvIG BAG API. It filters requests and enforces token-based authorization.

# Installation

Requirements:

* Python >= 3.13
* Recommended: Docker/Docker Compose (or pyenv for local installs)

## Using Docker Compose

Run docker compose:
```shell
docker compose up
```

Navigate to `localhost:8098`.


## Using Local Python

Create a virtualenv:

```shell
uv venv
source .venv/bin/activate
```

Install all packages in it:
```shell
make install  # alternatively you can use uv sync
```

Start the Django application:
```shell
uv run ./src/manage.py runserver localhost:8098
```

# Developer Notes

Run `make` in the root folder to have a help-overview of all common developer tasks.


## Package Management

Packages are managed with uv and locked in uv.lock.

To add a package: `uv add <package-name>`.
To add a development dependency: `uv add --dev <package-name>`.
This updates both pyproject.toml and uv.lock.

To upgrade dependencies, run `uv lock --upgrade`.
Then verify that everything still works with `uv sync && make test`.

## Environment Settings

Consider using *direnv* for automatic activation of environment variables.
In a similar way, uv helps to install the exact Python version, and will automatically activate a virtualenv and use it when you run commands using uv run.
It automatically sources an ``.envrc`` file when you enter the directory.
This file should contain all lines in the `export VAR=value` format.

The `.envrc.example` file contains an example of an environment variable that can be set.
Make sure to change this name to `.envrc` and run `direnv allow` to run pytest succesfully.


In a similar way, uv helps to install the exact Python version, and will automatically activate a virtualenv and use it when you run commands using `uv run`.

## Debugging

To debug a running container, run docker compose with the extra debug compose file:
```shell
docker compose -f docker-compose.yml -f docker-compose.debug.yml up -d
```

In your `.vscode` folder, copy the `launch.example.json` to `launch.json`. Ensure that the paths are matching with what you have (especially packages in your virtualenv).

Start the debugger through the Run and Debug menu. The debugger is called "Python Debugger: Remote Attach". You can now add breakpoints.
