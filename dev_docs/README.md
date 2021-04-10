# Installing the dependencies

You can set your environment up as you find most comfortable, but a good starting point is using virtual environments,
to find out more information about these, visit https://docs.python.org/3/tutorial/venv.html. But an even more
straight-forward method is using [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/index.html).

Whichever way you have chosen, a simple:


```shell
pip install -r requirements.txt
```

Should install all the requirements to execute the GC_database server and start the API.

# Running GC_database

To run the server go to the `GC_database` folder and execute:

```shell
python3 app.py
```

# Running the tests

There are different types of tests, the usual python tests and doctests. To run all the tests, you can simply:

```shell
pytest --doctest-modules
```

If you want a more automated development environment, it could be useful to install something like
[pytest-watch](https://pypi.org/project/pytest-watch/) which will re-run your tests when files change.

The command:
```shell
ptw -- --last-failed --new-first
```
should be all you need.