import requests

print("Attempting to connect to Finnhub.io...")

try:
    # We'll use Finnhub's simple "ping" endpoint
    response = requests.get("https://finnhub.io/api/v1/ping", timeout=5)

    if response.ok:
        print("\nSuccess! ✅ Python can connect to Finnhub.")
    else:
        print(f"\nFailed! Finnhub returned a bad status code: {response.status_code}")

except requests.exceptions.RequestException as e:
    print("\n--- CONNECTION FAILED --- ❌")
    print("This confirms the block is specific to Finnhub.io.")
    print("Error details:", e)