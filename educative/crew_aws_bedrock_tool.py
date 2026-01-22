@tool("LaptopTools")
def LaptopTools(question: str) -> str:
    """This expert has access to all details about the laptops we have in our inventory"""
    query = question
    client = boto3.client('bedrock-agent-runtime', region_name='us-east-1', aws_access_key_id='----',
                           aws_secret_access_key='----')
    model_arn = 'arn:aws:bedrock:us-east-1::foundation-model/<Model ID>'
    
    # Call the retrieve_and_generate API
    response = client.retrieve_and_generate(
        input={'text': query},
        retrieveAndGenerateConfiguration={
            'type': 'KNOWLEDGE_BASE',
            'knowledgeBaseConfiguration': {
                'knowledgeBaseId': '<Knowledge base ID>',
                'modelArn': model_arn
            }
        },
    )
    
    # Extract and return the output text
    output_data = response.get('output', {}).get('text', '')
    return output_data
