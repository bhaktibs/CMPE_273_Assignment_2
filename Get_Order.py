from __future__ import print_function
from boto3.dynamodb.conditions import Key, Attr
import boto3
import json
import time
import logging

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('order')
    menuId = table.get_item(
        Key ={
            'OderId': event['params']['path']['order_id']
        }
        )
    return menuId["Item"]