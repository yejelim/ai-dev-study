# test_requests.py
import requests

url = "http://127.0.0.1:8000/predict"
text = "큰거왔다"

try:
    response = requests.post(url, json={"text": text})
    response.raise_for_status()  # HTTP 오류 발생 시 예외 발생
except requests.exceptions.RequestException as e:
    print(f"요청 중 오류 발생: {e}")
    exit(1)

print("Status Code:", response.status_code)
print("Response JSON:", response.json())
