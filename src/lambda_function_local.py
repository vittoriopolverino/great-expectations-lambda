from lambda_local.main import call
from lambda_local.context import Context

import lambda_function

# test-event
event = {
    "payload": {"test_column": ["red", "yellow", "blue", "green"]}
}

# timeout in seconds (60)
context = Context(60)

if __name__ == '__main__':
    # Run lambda function on local machine
    call(lambda_function.handler, event, context)
