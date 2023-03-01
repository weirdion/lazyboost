.PHONY: default install dependency-prod dependency-develop dependency-update lint lint-ci package-check test test-html

# Run install-dep-develop job by default
default: dependency-develop

# Create a job that deploys this application to the system
install:
	poetry run pip instll -e .

# Create a job to install dependencies needed for production
dependency-prod:
	poetry install --no-dev

# Create a job to install dependencies needed for development
dependency-develop:
	poetry install

dependency-update:
	poetry update

# Create a job for running pytlint on the src
lint:
	 poetry run pylint ./src

# Create a modified job for CI for lint
lint-ci:
	 poetry run pylint --exit-zero ./src

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
