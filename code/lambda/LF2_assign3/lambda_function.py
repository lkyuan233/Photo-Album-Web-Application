import json
import boto3
import logging
import requests
from requests_aws4auth import AWS4Auth
import random

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
region = 'us-east-1'
service = 'es'
credentials = boto3.Session().get_credentials()
awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)

client = boto3.client('lexv2-runtime')

def lambda_handler(event, context):
    logger.debug(event)
    logger.debug(event['query'])
    response = client.recognize_text(
        botId='SB2SUQPIZZ',
        botAliasId='TSTALIASID',
        localeId='en_US',
        sessionId="test_session",
        text=event['query'])
    logger.debug(response)
    if response['messages']:
        labels = response['messages'][0]['content']
        labelsarr = labels.split(':')
        logger.debug(labelsarr[0])
        logger.debug(labelsarr[1])
        logger.debug(labelsarr[2])
        # search es
        headers = {"Content-Type": "application/json"}
        resp = ""
        if (len(labelsarr[2]) != 0):
            resp = requests.get('https://search-photos1-iuv6daakyhgj4uzyssc2sxw6qu.us-east-1.es.amazonaws.com/photos/photos/_search?from=0&&size=1&&q=labels:' + labelsarr[1],
            headers=headers, auth = awsauth).json()
            total = resp['hits']["total"]['value']
            select = random.randint(0, int(total) - 1)
            logger.debug(select)
            resp = requests.get('https://search-photos1-iuv6daakyhgj4uzyssc2sxw6qu.us-east-1.es.amazonaws.com/photos/photos/_search?from=' + str(select) + '&&size=1&&q=labels:' + labelsarr[1],
            headers=headers, auth=awsauth).json()
            logger.debug(resp)
        else:
            resp = requests.get('https://search-photos1-iuv6daakyhgj4uzyssc2sxw6qu.us-east-1.es.amazonaws.com/photos/photos/_search?from=0&&size=1&&q=labels:' + labelsarr[1],
            headers=headers, auth = awsauth).json()
            total = resp['hits']["total"]['value']
            select = random.randint(0, int(total) - 1)
            logger.debug(select)
            resp = requests.get('https://search-photos1-iuv6daakyhgj4uzyssc2sxw6qu.us-east-1.es.amazonaws.com/photos/photos/_search?from=' + str(select) + '&&size=1&&q=labels:' + labelsarr[1],
            headers=headers, auth=awsauth).json()
            logger.debug(resp)
    print(response)
    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
