import json
import boto3
import os
from boto3.dynamodb.conditions import Attr


class UserData:
    userId: str

    def __init__(self, code: str, uplandUserId: str, accessToken: str):
        self.code = code
        self.uplandUserId = uplandUserId
        self.accessToken = accessToken


def lambda_handler(event, context):

    if not isEventAuthenticated(event):
        return {
            "statusCode": 401
        }

    userDataToUpdate: UserData = getDataFromEvent(event)
    userDataToUpdate.userId = getUserIdFromCode(userDataToUpdate.code)
    updateUserData(userDataToUpdate)

    return {
        'statusCode': 200
    }

def updateUserData(user: UserData):

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ['TABLE_NAME'])
    table.update_item(
        Key={
            "EpicAccountId":user.userId
        },
        UpdateExpression='SET code = :code, uplandUserId = :uplandUserId, accessToken = :accessToken',
        ExpressionAttributeValues={
        ':code': "",
        ':uplandUserId': user.uplandUserId,
        ':accessToken': user.accessToken
        }
    )
    return

def getUserIdFromCode(code):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ['TABLE_NAME'])

    response = table.scan()

    userWithCode = []

    for item in response['Items']:
        if item['code'] == code:
            userWithCode.append(item)

    if len(userWithCode) != 1:
        raise Exception("Too many users with the same code")

    print(userWithCode[0])
    return userWithCode[0]['EpicAccountId']


def isEventAuthenticated(event):

    token = event['headers']['Authorization']
    token = token.replace("Bearer ", "")
    return token == os.environ['UPLAND_WEBHOOK_TOKEN']

def getDataFromEvent(event):

    try:

        body = json.loads(event['body'])
        code = body['data']['code']
        uplandUserId = body['data']['userId']
        accessToken = body['data']['accessToken']

        return UserData(code, uplandUserId, accessToken)
    except Exception as e:
        raise e