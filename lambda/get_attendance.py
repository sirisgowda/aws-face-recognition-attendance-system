import json
import boto3

dynamodb = boto3.resource("dynamodb")

TABLE = "Attendance"

def lambda_handler(event, context):

    table = dynamodb.Table(TABLE)

    response = table.scan()

    return {

        "statusCode":200,

        "headers":{

            "Access-Control-Allow-Origin":"*"

        },

        "body":json.dumps(response.get("Items",[]))

    }