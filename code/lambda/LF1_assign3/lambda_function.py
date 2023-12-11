# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

"""
Purpose
An AWS lambda function that analyzes images with an the Amazon Rekognition
Custom Labels model.
"""
import json
import base64
from os import environ
import logging
import boto3

from botocore.exceptions import ClientError

import requests
from requests_aws4auth import AWS4Auth
from datetime import datetime

# Set up logging.
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Get the model ARN and confidence.
model_arn = environ['MODEL_ARN']
min_confidence = int(environ.get('CONFIDENCE', 50))

# Get the boto3 client.
rek_client = boto3.client('rekognition')

esurl = 'https://search-photos1-iuv6daakyhgj4uzyssc2sxw6qu.us-east-1.es.amazonaws.com/photos/photos'
headers = {"Content-Type": "application/json"}
region = 'us-east-1'
service = 'es'
credentials = boto3.Session().get_credentials()
awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)

def lambda_handler(event, context):
    """
    Lambda handler function
    param: event: The event object for the Lambda function.
    param: context: The context object for the lambda function.
    return: The labels found in the image passed in the event
    object.
    """

    try:

        # Determine image source.
        if 'image' in event['Records'][0]:
            # Decode the image
            image_bytes = event['image'].encode('utf-8')
            img_b64decoded = base64.b64decode(image_bytes)
            image = {'Bytes': img_b64decoded}


        elif 's3' in event['Records'][0]:
            logger.info(event['Records'][0]['s3']['bucket']['name'])
            logger.info(event['Records'][0]['s3']['object']['key'])
            image = {
                'S3Object': {
                    'Bucket': event['Records'][0]['s3']['bucket']['name'],
                    'Name': event['Records'][0]['s3']['object']['key']
                }
            }
        else:
            logger.info(event)
            raise ValueError(
                'Invalid source. Only image base 64 encoded image bytes or S3Object are supported.')


        # Analyze the image.
        response = rek_client.detect_custom_labels(Image=image,
            ProjectVersionArn=model_arn)
        
        logger.info(response)

        # Get the custom labels
        labels = response['CustomLabels']
        logger.info(labels)
        newLabels = []

        for l in labels:
            newLabels.append(l['Name'])
        logger.info(newLabels)
        
        currentDateAndTime = datetime.now()
        currentTime = currentDateAndTime.strftime('%Y-%m-%dT%H:%M:%S')
        body = {"objectKey":event['Records'][0]['s3']['object']['key'],
            "bucket":event['Records'][0]['s3']['bucket']['name'],
            "createdTimestamp":currentTime,
            "labels":newLabels
        }
        r = requests.post(esurl,
            data=json.dumps(body).encode("utf-8"),
            headers=headers,
            auth=awsauth)
        logger.info(json.dumps(r.json()))
        lambda_response = {
            "statusCode": 200,
            "body": json.dumps(labels)
        }

    except ClientError as err:
        error_message = f"Couldn't analyze image. " + \
            err.response['Error']['Message']

        lambda_response = {
            'statusCode': 400,
            'body': {
                "Error": err.response['Error']['Code'],
                "ErrorMessage": error_message
            }
        }
        logger.error("Error function %s: %s",
            context.invoked_function_arn, error_message)

    except ValueError as val_error:
        lambda_response = {
            'statusCode': 400,
            'body': {
                "Error": "ValueError",
                "ErrorMessage": format(val_error)
            }
        }
        logger.error("Error function %s: %s",
            context.invoked_function_arn, format(val_error))

    return lambda_response
