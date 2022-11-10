import json
import urllib3
import boto3
import os
import uuid

applicationId = str(os.environ['UPLAND_APP_ID'])
uplandConnectionCodeEndpoint = str(os.environ['UPLAND_NEW_CODE_ENDPOINT'])

class ApplicationNotAuthorized(Exception):
    def __init__(self, message="The applicationId is not authorized in upland"):
        self.errorMessage = message
        super().__init__(self.errorMessage)


def lambda_handler(event, context):
    code = getNewCode()

    #! 'userId' can be set if you need to pair your application's User Id to upland's
    userId = uuid.uuid4()

    updateTableCode(code, userId)

    return {
        "statusCode": 200,
        "body": json.dumps({
            "code": code
        })
    }

def updateTableCode(code: str, userId: str):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ['TABLE_NAME'])
    table.update_item(
        Key={
            'id':userId
        },
        UpdateExpression='SET code = :values',
        ExpressionAttributeValues={
        ':values': code
        }
    )
    return

def updateUserCode(code, token):

    cognitoClient = boto3.client('cognito-idp')

    cognitoClient.update_user_attributes(
        UserAttributes=[
            {
                'Name': 'custom:uplandCode',
                'Value': code
            },
        ],
        AccessToken=token
    )

def getNewCode():

    global applicationId
    global uplandConnectionCodeEndpoint
    appAccessToken = os.environ['UPLAND_APPLICATION_ACCESS_TOKEN']

    http = urllib3.PoolManager()
    headers = urllib3.make_headers(
        basic_auth = applicationId + ':' + appAccessToken
        )

    codeResponse = http.request(
        'POST', uplandConnectionCodeEndpoint, headers=headers)
    if codeResponse.status == 401:
        raise ApplicationNotAuthorized
    elif codeResponse.status != 201:
        raise ApplicationNotAuthorized(str(codeResponse.status) + str(codeResponse.data))
    data = json.loads(codeResponse.data)

    return data.get("code")