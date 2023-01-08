import boto3
from flask import *
from boto3.dynamodb.conditions import Key, Attr


accessKeyId="AKIAV74HG75A2HCLM3P5"
accessSecretKey="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"
# sessionToken = "FwoGZXIvYXdzEAMaDDkxmdCmHh96i30krCLGAfihSy8ku6hHKRnbOCAXirVUJG70EitE9c2EO44YJq8+4ma/pqiIEnWX3ZR20Qi2U4KCTUSiqqCOzjF3O9viNJaQv0MKEcjE3TY768CzQn6YWQXeKZWyN7Lp4efvnXx1rUssQodqMA3LlxB6Eb0/HxtJ50qUdUijSOZONz3QcpLqej6G74FJAd+cRnhIajMlz79orT2A2528tYmIS+Da/2VyLsM4+VevpzJI6G5eHZPKK9OiGgfdKQUCAU8dZmYZs+T7eaZifyjKw66dBjItj7KW/9DuioqL4qmRvnvrJD4pE/YAh1TkUc6+fjrtiX2ExzTdLpVc/qp+zYFd"
dynamodb = boto3.resource('dynamodb', aws_access_key_id=accessKeyId, aws_secret_access_key=accessSecretKey, region_name = 'us-east-1')



def insert(items):
    try:
        table = dynamodb.Table('doggy')
        table.put_item(
            Item = {
                'id' : items[0],
                'name': items[1],
                'info' : items[2],
                'img' : items[3],
            }
        )
        print("add table success!")
    except:
        print("add table failed")

#[userId, _id, name, birthDate, sex, petNumber, type, imgUrl]
def insertPet(items):
    try:
        # if items[3]=="" or items[5]=="" or items[6]==""
        table = dynamodb.Table('pet_info')
        table.put_item(
            Item = {
                'user_id': items[0],
                'id' : items[1],
                'pet_name': items[2],
                'birth' : items[3],
                'sex' : items[4],
                'chip_number': items[5],
                'pet_type': items[6],
                'img': items[7]
            }
        )
        print("add to table pet_info success!")
    except:
        print("add to table pet_info failed")


def deletePet(user, _id):
    table = dynamodb.Table('pet_info')
    try:
        response = table.delete_item(
            Key={
                'user_id': user,
                'id': _id,
            }
        )
        return True
    except:
        return False

def ShowDogType(_id):
    table = dynamodb.Table('doggy')
    response = table.query(
        TableName = 'doggy',
        KeyConditions = {
            'id': {
                'AttributeValueList': [
                    _id
                ],
                'ComparisonOperator': 'EQ'
            }
        }
    )
    return response['Items']

def ShowAll():
    table = dynamodb.Table('doggy')
    response = table.scan(
        TableName = 'doggy'
    )
    return response['Items']


# TODO: Query 時效 (strptime)
    # def expired()
    # def not_expired()

# TODO: Query 關鍵字(if I have time)


def update(_id, img):
    table = dynamodb.Table('doggy')
    table.update_item(
        Key={
            'id': _id
        },
        UpdateExpression="SET img= :s1",
        ExpressionAttributeValues={
                    ':s1': img,
                    },
        ReturnValues="UPDATED_NEW"
    )
    print('修改完成')

def updatePet(pet):
    table = dynamodb.Table('pet_info')
    table.update_item(
        Key={
            'user_id': pet[0],
            'id': pet[1]
        },
        UpdateExpression="SET pet_name= :s1, birth= :s2, sex= :s3, chip_number= :s4, pet_type= :s5, img= :s6",
        ExpressionAttributeValues={
                    ':s1': pet[2],
                    ':s2': pet[3],
                    ':s3': pet[4],
                    ':s4': pet[5],
                    ':s5': pet[6],
                    ':s6': pet[7]
                    },
        ReturnValues="UPDATED_NEW"
    )
    print('修改pet完成')


def ShowAllPet(user):
    table = dynamodb.Table('pet_info')
    response = table.query(
        KeyConditionExpression=Key('user_id').eq(user)
    )
    return response['Items']

def ShowPet(user, _id):
    table = dynamodb.Table('pet_info')
    response = table.query(
        KeyConditionExpression=Key('user_id').eq(user) & Key('id').eq(_id)
    )
    return response['Items']




def keywords(user, word):
    table = dynamodb.Table('pet_info')
    response = table.query(
        KeyConditionExpression=Key('userid').eq(user),
        FilterExpression = 'contains(#date, :name) or contains(#name, :name) or contains(#place, :name) or contains(#type, :name)',
        ExpressionAttributeNames = {
            '#date': 'itemDate',
            '#name': 'itemName',
            '#place': 'itemPlace',
            '#type': 'itemType',
        },
        ExpressionAttributeValues = {
            ':name': word,
        }
    )
    return response['Items']
