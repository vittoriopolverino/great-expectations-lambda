FROM public.ecr.aws/lambda/python:3.9

COPY lambda_function.py ${LAMBDA_TASK_ROOT}
COPY src ${LAMBDA_TASK_ROOT}/src
COPY local/lambda_function_local.py ${LAMBDA_TASK_ROOT}/src
COPY local/event.json ${LAMBDA_TASK_ROOT}
COPY great_expectations ${LAMBDA_TASK_ROOT}/great_expectations

# Install the function's dependencies using file requirements.txt from your project folder.
COPY requirements.txt .

RUN pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}/src"

# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD ["lambda_function.handler"]
