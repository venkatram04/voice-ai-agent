import boto3
import json

from app.config import (
    AWS_ACCESS_KEY_ID,
    AWS_SECRET_ACCESS_KEY,
    AWS_REGION
)

bedrock_runtime = boto3.client(
    service_name="bedrock-runtime",
    region_name=AWS_REGION,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)


async def ask_nova(user_message):

    prompt = f"""
You are a helpful hospital voice assistant.

Your tasks:
- greet users naturally
- help with appointments
- answer doctor availability
- correct speech mistakes
- keep replies short and natural

Available doctors:
- Dr Kumar (Cardiologist)
- Dr Priya (Dermatologist)
- Dr Ahmed (General Physician)

Reply conversationally.

User:
{user_message}
"""

    body = {
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
            "maxTokens": 200,
            "temperature": 0.7
        }
    }

    response = bedrock_runtime.invoke_model(
        modelId="amazon.nova-lite-v1:0",
        body=json.dumps(body)
    )

    response_body = json.loads(
        response["body"].read()
    )

    output = response_body[
        "output"
    ]["message"]["content"][0]["text"]

    return output