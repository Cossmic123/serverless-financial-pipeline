# backend/local_test.py
import os
import json
from dotenv import load_dotenv

# --- 1. Load .env FIRST (before importing lambda_processor) ---
load_dotenv()

# --- 2. Import lambda_processor AFTER environment is set ---
from lambda_processor import lambda_handler

# --- 3. Create a Mock SNS Event ---
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

# --- 4. Call the Lambda Handler ---
if __name__ == "__main__":
    print("--- Running Local Test with Polygon.io ---")
    result = lambda_handler(mock_sns_event, None)
    print("\n--- Function Result ---")
    print(result)