# backend/lambda_orchestrator.py

import json
import boto3
import os

SNS_TOPIC_ARN = os.environ.get('SNS_TOPIC_ARN', '')
sns_client = boto3.client('sns')

def lambda_handler(event, context):
    # Your health check, correctly placed in the API-facing Lambda
    if event.get("path") == "/health":
        return {
            "statusCode": 200,
            "headers": {
                'Access-Control-Allow-Origin': '*',
                "Content-Type": "application/json"
            },
            "body": json.dumps({"status": "OK"})
        }

    # The main logic to start the pipeline
    try:
        body = json.loads(event.get('body', '{}'))
        tickers = body.get("tickers", [])

        if not tickers:
            return {'statusCode': 400, 'body': json.dumps('Error: No tickers provided.')}

        for ticker in tickers:
            message = {"ticker": ticker}
            sns_client.publish(
                TopicArn=SNS_TOPIC_ARN,
                Message=json.dumps(message)
            )
            
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': json.dumps(f'Successfully published {len(tickers)} tasks.')
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps(f'Error: {str(e)}')}