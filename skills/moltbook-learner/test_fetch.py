import requests
import json

API_KEY = "moltbook_sk_mBZlubCuTFQcbh1M-XQH3NI8Fy23i_u5"

try:
    resp = requests.get(
        "https://www.moltbook.com/api/v1/feed",
        headers={"Authorization": f"Bearer {API_KEY}"},
        params={"limit": 10},
        timeout=30
    )
    with open("C:\\Users\\贾若\\.openclaw\\workspace\\skills\\moltbook-learner\\data\\posts\\live_fetch.json", "w", encoding="utf-8") as f:
        f.write(resp.text)
    print("Done")
except Exception as e:
    with open("C:\\Users\\贾若\\.openclaw\\workspace\\skills\\moltbook-learner\\data\\posts\\error.txt", "w") as f:
        f.write(str(e))
    print("Error:", e)
