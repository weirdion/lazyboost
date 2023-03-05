FROM public.ecr.aws/lambda/python:3.9

# Install poetry
RUN pip install poetry

# Copy only requirements to cache them in docker layer
WORKDIR ${LAMBDA_TASK_ROOT}
COPY poetry.lock pyproject.toml README.md ${LAMBDA_TASK_ROOT}/

# Project init with --no-root so it's cached
RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi --no-root

# Copy the app to the Docker image
COPY src ${LAMBDA_TASK_ROOT}/src

# Install application code
RUN poetry install --no-interaction --no-ansi

# Lambda handler
CMD [ "src.lazyboost.index.order_sync_handler" ]
