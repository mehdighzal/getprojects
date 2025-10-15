import requests

print("Testing network access...")
print("=" * 50)

# Test backend
try:
    response = requests.get('http://10.0.6.141:8000/api/auth/me/', timeout=5)
    print(f"Backend (10.0.6.141:8000): Status {response.status_code}")
    if response.status_code == 401:
        print("SUCCESS: Backend accessible (401 expected without auth)")
    else:
        print("ERROR: Backend issue")
except Exception as e:
    print(f"ERROR: Backend error: {str(e)}")

# Test frontend
try:
    response = requests.get('http://10.0.6.141:3001/', timeout=5)
    print(f"Frontend (10.0.6.141:3001): Status {response.status_code}")
    if response.status_code == 200:
        print("SUCCESS: Frontend accessible")
    else:
        print("ERROR: Frontend issue")
except Exception as e:
    print(f"ERROR: Frontend error: {str(e)}")

print("=" * 50)
print("If both show SUCCESS, other devices should be able to access:")
print("Frontend: http://10.0.6.141:3001")
print("Backend: http://10.0.6.141:8000")
