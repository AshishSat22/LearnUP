import urllib.request
import json

req = urllib.request.Request(
    'http://127.0.0.1:5000/api/chat', 
    data=json.dumps({"message": "test context", "history": []}).encode('utf-8'), 
    headers={'Content-Type': 'application/json'}, 
    method='POST'
)

try:
    with urllib.request.urlopen(req) as response:
        print("SUCCESS:", response.read().decode())
except urllib.error.HTTPError as e:
    print(f"HTTP Error {e.code}: {e.read().decode()}")
except Exception as e:
    print("ERROR:", e)
