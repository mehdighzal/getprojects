import requests

print("Debugging backend issue...")
try:
    response = requests.get('http://10.0.6.141:8000/api/auth/me/', timeout=5)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text[:500]}")
except Exception as e:
    print(f"Error: {str(e)}")
