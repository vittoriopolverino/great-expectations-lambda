import expectations


def handler(event, context):
    print("hello World, i'm a containerized Lambda function")
    event_payload = event['payload']
    expectations_result = expectations.run(data=event_payload)

    return {
        "statusCode": 200,
        "body": expectations_result
    }


