import os
import boto3
import pytest
from moto import mock_aws
from hello_world.app import handler

@mock_aws
def test_lambda_handler():
    # 1. Configurar o ambiente de "teatro" (Mock)
    os.environ['AWS_DEFAULT_REGION'] = 'eu-west-3'
    dynamodb = boto3.resource('dynamodb', region_name='eu-west-3')
    
    # 2. Criar a tabela idêntica à real
    dynamodb.create_table(
        TableName='VisitorCounter',
        KeySchema=[{'AttributeName': 'id', 'KeyType': 'HASH'}],
        AttributeDefinitions=[{'AttributeName': 'id', 'AttributeType': 'S'}],
        BillingMode='PAY_PER_REQUEST'
    )

    # 3. Chamar a tua função (O teste real)
    ret = handler(None, None)

    # 4. Verificar os resultados (Assertions)
    assert ret['statusCode'] == 200
    assert 'count' in ret['body']
    
    # O primeiro acesso deve ser 1
    import json
    data = json.loads(ret['body'])
    assert data['count'] == 1