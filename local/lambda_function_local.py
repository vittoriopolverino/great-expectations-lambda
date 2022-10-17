import json
import os
import sys

from lambda_local.context import Context
from lambda_local.main import call

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import lambda_function

# timeout in seconds (60)
context = Context(60)

if __name__ == "__main__":
    with open("event.json", "r") as f:
        event = json.load(f)

    # Run lambda function on local machine
    call(lambda_function.handler, event, context)
