import json
import boto3

# Inicializa o comando à distância para o DynamoDB
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('VisitorCounter')

def handler(event, context):
    # 1. O "Click" Atómico: Incrementa o contador sem precisar de ler primeiro
    response = table.update_item(
        Key={'id': 'visits'},
        UpdateExpression='ADD #c :val',
        ExpressionAttributeNames={'#c': 'count'},
        ExpressionAttributeValues={':val': 1},
        ReturnValues='UPDATED_NEW'
    )
    
    # 2. Extrai o novo valor
    new_count = response['Attributes']['count']

    # 3. Responde ao Browser (com um "olá" para as CORS)
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': 'https://afonsom.dev', # Importante para o seu site conseguir ler
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Methods': 'GET'
        },
        'body': json.dumps({'count': int(new_count)})
    }