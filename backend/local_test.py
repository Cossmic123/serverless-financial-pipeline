# backend/local_test.py
import os
import json
from lambda_processor import lambda_handler

# --- 1. Set Up Mock Environment Variables ---
os.environ['POLYGON_API_KEY'] = "Ip4w1zknVXNQu6NlneYFsWIoAEz1pROj"
os.environ['S3_BUCKET_NAME'] = "dummy-bucket-name"

# --- 2. Create a Mock SNS Event ---
# This simulates the message the worker would get from SNS
mock_sns_event = {
    "Records": [
        {
            "Sns": {
                "Message": json.dumps({"ticker": "MSFT"}) # Testing with Microsoft
            }
        }
    ]
}

# --- 3. Call the Lambda Handler ---
if __name__ == "__main__":
    print("--- Running Local Test with Polygon.io ---")
    result = lambda_handler(mock_sns_event, None)
    print("\n--- Function Result ---")
    print(result)