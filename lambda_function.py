import pandas as pd

import expectations_example as expectations


def handler(event, context):
    print("hello World, i'm a containerized Lambda function")
    event_payload = event["payload"]
    expectations.run(data_frame=pd.DataFrame(event_payload))

    return {"statusCode": 200}
