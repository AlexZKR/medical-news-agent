run_local:
	export PYTHONPATH=$(PWD) && . venv/bin/activate && streamlit run medicalagent/drivers/main.py

requirements:
	. venv/bin/activate && python -m pip install --upgrade pip setuptools wheel && python -m pip install -r requirements.txt

# Linting
lint: mypy ruff bandit

mypy:
	mypy . --check-untyped-defs

ruff:
	ruff check --config pyproject.toml --fix

bandit:
	bandit -c pyproject.toml -r . --quiet

# Formatting
format:
	ruff format --config pyproject.toml .

# Testing
check: lint tests

tests:
	PYTHONPATH=$(PWD) \
	&& . venv/bin/activate \
	&& pytest --cov --cov-fail-under=90 --cov-report html

coverage:
	PYTHONPATH=$(PWD) \
	&& . venv/bin/activate \
	&& python -m webbrowser -t htmlcov/index.html
