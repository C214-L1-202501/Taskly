## Activating the virtual environment (venv)
From inside the IDE, open the terminal in the root of the system and run:
```shell
./venv/Scripts/activate.ps1
```

## Installing dependencies
````shell
pip install -r requirements.txt
````

## Commit Configuration

After to install requirements, you must configure ``pre-commit`` to maintain a code standard of our team.
To do this, you must run the following command:

```shell
pre-commit install
```

This command will configure a routine in a commit process to block a code out of code standard preset.

If you commit blocks by ``pre-commit process``, you need to see the git console in pycharm to be 
able to adjust the errors accused by linting.

You must run the following commands before commit to avoid block commits:

### Black

```shell
# this command list and format all files
black .

# OR

# this command list and format all files and shows what he changed in each file
black . --diff

# OR

# this command only check and list files that need to reformat
black . --check
```

### Isort

```shell
# this command organizes all imports following one order
# --------------------------------
# Built-in functions
# Externals packages
# Project Modules
# --------------------------------
isort .

# OR 

# this command shows files to reformat imports your self
isort . --check

# OR 

# this command shows files to reformat imports and what you must changed in each file
isort . --check --diff
```

### Flake8

After running the above commands, run following command, it will check all files on your project 
and shows errors based on [PEP8](https://peps.python.org/pep-0008/).
```shell
flake8 .
```

### Running Automated Tests

To run the automated tests, you need to be in the root directory of the project.

Run the following command in your terminal:

```shell
python -m pytest -v tests
```

This will execute all the tests located in the `tests/` directory.

Make sure you have `pytest` installed before running the tests. If you don't have it installed, you can install it using:

```shell
pip install pytest
```