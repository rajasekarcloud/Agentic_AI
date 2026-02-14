import json
import boto3

def lambda_handler(event, context):
    client = boto3.client('bedrock-runtime')
    prompt = event.get(
        'prompt',
        'Provide three key benefits of using Amazon Nova Micro for text generation.'
    )

    model_id = 'us.amazon.nova-micro-v1:0'
    payload = {
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "text": prompt
                    }
                ]
            }
        ],
        "inferenceConfig": {
            "max_new_tokens": 512,
            "temperature": 0.7,
            "top_p": 0.9
        }
    }

    response = client.invoke_model(
        modelId=model_id,
        body=json.dumps(payload),
        accept='application/json',
        contentType='application/json'
    )

    response_json = json.loads(response['body'].read())
    result = response_json['output']['message']['content'][0]['text']
    print(result)

    return {
        'statusCode': 200,
        'body': json.dumps(result)
    }
