import requests
import json
from fastapi import HTTPException
# Base64 text file
BASE64_FILE = r"C:\Users\Hello\Desktop\table_data_extractor\base64_text_files\hdfc.txt"

# Output JSON file
OUTPUT_FILE = "hdfc.json"

# API URL
URL = "http://127.0.0.1:8000/extract-table"

# Read Base64 from text file
with open(BASE64_FILE, "r", encoding="utf-8") as f:
    pdf_base64 = f.read().strip()

# Request payload
payload = {
    "file_name": "hdfc",
    "pdf_base64": pdf_base64
}

# Send request
response = requests.post(
    URL,
    headers={"Content-Type": "application/json"},
    json=payload
)

print("Status Code:", response.status_code)

# Save response
try:
    response_json = response.json()

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(
            response_json,
            f,
            indent=4,
            ensure_ascii=False
        )

    print(f"Response saved to {OUTPUT_FILE}")

# except Exception:
#     print("Response is not JSON")
#     print(response.text)
except Exception as e:
    import traceback
    traceback.print_exc()
    raise HTTPException(
        status_code=500,
        detail=str(e)
    )