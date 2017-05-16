from __future__ import print_function
from boto3.dynamodb.conditions import Key, Attr
import boto3
import json

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('order')
    print(event['order_id'])
    table.put_item(Item={'OderId':event['order_id'],'menu_id':event['menu_id'],'customer_name':event['customer_name'],'customer_email':event['customer_email']})
    response = {
            "Message": "Hi "+event['customer_name']+", please choose one of these selection:  1. Cheese, 2. Pepperoni, 3.Vegetable"
        }