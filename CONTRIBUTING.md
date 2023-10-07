# Contributing

Thank you for investing your time in contributing to **KEBA KeEnergy API**.

## Setting up an environment

Clone the `KEBA-KeEnergy-API` repository.
Inside the repository, create a virtual environment:

```bash
python3 -m venv .venv
```

Activate the virtual environment:

```bash
source .venv/bin/activate
```

Install the development dependencies:

```bash
pip install -e ".[lint,format,audit,tests]"
```

## Testing

To test the code we use [pytest](https://docs.pytest.org):

```bash
pytest -n auto
```

To get the full test coverage report of `KEBA-KeEnergy-API`, run the following command:

```bash
pytest --cov-report term-missing --cov=keba_keenergy_api
```

## Making a pull request

When you're finished with the changes, create a pull request, also known as a PR.
The branch to contribute is `main`. Please also update the [CHANGELOG.md](CHANGELOG.md) with your changes.
