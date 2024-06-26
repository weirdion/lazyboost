.PHONY: default install dependency-prod dependency-update lint lint-ci package-check test test-html

# Run install job by default
default: install

# Create a job that deploys this application to the system
install:
	poetry install

# Create a job to install dependencies needed for production
dependency-prod:
	poetry install --no-dev

dependency-update:
	poetry update
	npm update

# Create a job for running pytlint on the src
lint:
	 poetry run black ./src && poetry run isort ./src

# Create a modified job for CI for lint
lint-ci:
	 poetry run black --check ./src

# Create a job to check for vulnerable packages installed
package-check:
	poetry run safety check

# Create a job for running tests on src folder and print coverage to cli
test:
	PYTHONPATH=./src poetry run pytest tests --doctest-modules --cov=lazyboost

# Create a job to run pytest on src folder and generate coverage into xml and html
test-html:
	PYTHONPATH=./src poetry run pytest tests --doctest-modules --junitxml=junit/test-results.xml \
	    --cov=lazyboost --cov-report=xml --cov-report=html
