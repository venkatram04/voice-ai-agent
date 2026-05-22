import boto3
import json
import traceback

from app.config import AWS_REGION

bedrock = boto3.client(
    service_name="bedrock-runtime",
    region_name=AWS_REGION
)

MODEL_ID = "amazon.nova-lite-v1:0"

def ask_bedrock(prompt):

    try:

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
                "maxTokens": 300,
                "temperature": 0.7
            }
        }

        response = bedrock.invoke_model(
            modelId=MODEL_ID,
            body=json.dumps(body)
        )

        response_body = json.loads(
            response["body"].read()
        )

        return response_body["output"]["message"]["content"][0]["text"]

    except Exception as e:

        print("\n========== BEDROCK ERROR ==========\n")

        traceback.print_exc()

        print("\n===================================\n")

        return f"Bedrock Error: {str(e)}"