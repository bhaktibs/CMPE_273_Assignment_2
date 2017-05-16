from __future__ import print_function
from boto3.dynamodb.conditions import Key, Attr
import boto3
import json
import time
import logging

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    input_choice = int(event['body-json']['input'])
    table=dynamodb.Table('order')
    menuId = table.get_item(
        Key ={
            'OderId': event['params']['path']['order_id']
            
        },
        ProjectionExpression='menu_id'
        )
    selection = table.get_item(
        Key ={
            'OderId': event['params']['path']['order_id']
            
            
        },
        ProjectionExpression='selection'
        )
    selected_item =selection["Item"]
    print(selected_item)
    table2 = dynamodb.Table('Menu')
    if(selection["Item"]=={}):
        print ("in one")
        
        choices = table2.get_item(
            Key ={
                'menu_id':menuId["Item"]["menu_id"]
            },
            ProjectionExpression='selection'
            )
        set_selection = choices["Item"]["selection"]
        list_selection = list(set_selection)
        pizza_choice = list_selection[input_choice-1]
        result = table.update_item(
            Key={
                'OderId': event['params']['path']['order_id']
            },
            UpdateExpression='set selection = :r',
            ExpressionAttributeValues={
                ':r':pizza_choice
            }
            )
        sizes = table2.get_item(
            Key ={
                'menu_id':menuId["Item"]["menu_id"]
            },
            ProjectionExpression='size'
            )
        set_sizes = sizes["Item"]["size"]
        list_sizes = list(set_sizes)
        Message= "Which size do you want? "
        i=1
        for l in list_sizes:
                Message = Message + " "+str(i)+". "+list_sizes[i-1]+" ,"
                i+=1
        response = {
            "Message": Message
        }
        return response
        
    else:
        size_choices = table2.get_item(
            Key ={
                'menu_id':menuId["Item"]["menu_id"]
            },
            ProjectionExpression='size'
            )
        set_size = size_choices["Item"]["size"]
        list_size = list(set_size)
        size_choice = list_size[input_choice-1]
        prices = table2.get_item(
            Key ={
                'menu_id':menuId["Item"]["menu_id"]
            },
            ProjectionExpression='price'
            )
        set_prices = prices["Item"]["price"]
        list_prices = list(set_prices)
        list_prices.sort()
        if(input_choice==1):
            costs=15
        elif(input_choice==2):
            costs=7
        elif(input_choice==3):
            costs=3.5
        elif(input_choice==4):
            costs=10
        elif(input_choice==5):
            costs=20
        timestamp = int(time.time() * 1000)
        processing="processing"
        result = table.update_item(
            Key={
                'OderId': event['params']['path']['order_id']
            },
            UpdateExpression='set cost = :r, '
                            'order_status = :check, '
                            'updatedAt = :updatedAt,'
                            'size = :sizeSelected',
            ExpressionAttributeValues={
                ':r':costs,
                ':updatedAt':timestamp,
                ':check':processing,
                ':sizeSelected':size_choice
            }
            )
        response = {
            "Message": "Your order costs $"+str(costs)+". We will email you when the order is ready. Thank you!"
        }
        return response