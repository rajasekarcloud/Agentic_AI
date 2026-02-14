import json
import logging
import boto3
from botocore.exceptions import ClientError
import base64

logger = logging.getLogger(__name__)

bedrock_runtime_client = boto3.client('bedrock-runtime', region_name='us-east-1')

def lambda_handler(event, context):
    if (
        "queryStringParameters" not in event or
        "prompt" not in event["queryStringParameters"]
    ):
        return {
            'statusCode': 400,
            'body': generate_html(None, None, 'Pass in the "prompt" query parameter'),
            'headers': {
                'Content-Type': 'text/html',
            }
        }

    prompt = event["queryStringParameters"]["prompt"]
    image_data = invoke_nova_canvas(prompt)

    return {
        'statusCode': 200,
        'body': generate_html(prompt, image_data),
        'headers': {
            'Content-Type': 'text/html',
        },
    }

def invoke_nova_canvas(prompt, style_preset=None):
    try:
        body = json.dumps({
            "taskType": "TEXT_IMAGE",
            "textToImageParams": {
                "text": prompt
            },
            "imageGenerationConfig": {
                "numberOfImages": 1,
                "quality": "standard",
                "height": 768,
                "width": 768,
                "seed": 100
            }
        })
        response = bedrock_runtime_client.invoke_model(
            modelId="amazon.nova-canvas-v1:0",
            accept="application/json",
            contentType="application/json",
            body=body
        )

        response_body = json.loads(response["body"].read())
        image_data = response_body["images"][0]

        return image_data

    except ClientError:
        logger.error("Failed to invoke model")
        raise

def generate_html(prompt, image_data, error=None):
    if error:
        response = """
            <h2>{0}</h2>
            <h3>{1}</h3>
        """.format(error, "Example: ?prompt=three little birds")
    else:
        response = """
            <h3>Prompt: {0}</h3>
            <img src="{1}" alt="Base64 Image">
        """.format(prompt, f"data:image/png;base64,{image_data}")

    return """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Amazon Bedrock - Nova Canvas Model</title>
        </head>
        <body style="text-align:center">
            {0}
        </body>
        </html>
    """.format(response)
