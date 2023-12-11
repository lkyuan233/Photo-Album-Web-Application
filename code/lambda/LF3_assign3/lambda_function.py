import json
import logging

logger = logging.getLogger()

    
def lambda_handler(event, context):

    return dispatch(event)

def dispatch(request):
    intent = request['sessionState']['intent']['name']
    if intent == 'SearchIntent':
        return handle_search(request)
    else:
        return {
        'sessionState': {
            'dialogAction': {
                'type': 'ElicitIntent'
            }
        },
        'messages': [
            {
                'contentType': 'PlainText',
                'content': 'Not Valid'
            }
        ]
    }
        

def handle_search(request):
    label1 = request['sessionState']['intent']['slots']['labels1']['value']['resolvedValues'][0]
    label2 = ''
    if request['sessionState']['intent']['slots']['labels2']:
        label2 = request['sessionState']['intent']['slots']['labels2']['value']['resolvedValues'][0]

    return {
        'sessionState': {
            'dialogAction': {
                'type': 'ElicitIntent'
            }
        },
        'messages': [
            {
                'contentType': 'PlainText',
                'content': 'labels:' + label1 + ':' + label2
            }
        ]
    }

