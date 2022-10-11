import src.expectations_example as expectations


def handler(event, context):
    print("hello World, i'm a containerized Lambda function")
    event_payload = event["payload"]
    expectations.run(data=event_payload)

    return {"statusCode": 200}
