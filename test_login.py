#!/usr/bin/env python3
import requests
import json

# API base URL
BASE_URL = "http://localhost:8000"

def test_seed_data():
    """Test seeding data"""
    try:
        response = requests.post(f"{BASE_URL}/seed_data")
        print(f"Seed data response: {response.status_code}")
        if response.text:
            print(f"Response: {response.text}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error seeding data: {e}")
        return False

def test_login(email, password):
    """Test login functionality"""
    try:
        # Prepare form data for OAuth2PasswordRequestForm
        form_data = {
            'username': email,
            'password': password
        }
        
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        
        print(f"Testing login for: {email}")
        response = requests.post(f"{BASE_URL}/token", data=form_data, headers=headers)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            token_data = response.json()
            print(f"Login successful! Token: {token_data.get('access_token', 'No token')[:50]}...")
            return True
        else:
            print(f"Login failed: {response.text}")
            return False
            
    except Exception as e:
        print(f"Error during login test: {e}")
        return False

def test_health():
    """Test health endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Health check: {response.status_code} - {response.text}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error in health check: {e}")
        return False

if __name__ == "__main__":
    print("=== Testing Backend API ===")
    
    print("\n1. Health Check:")
    test_health()
    
    print("\n2. Seeding Database:")
    test_seed_data()
    
    print("\n3. Testing Login with demo credentials:")
    # Test with the demo credentials from the seeded data
    test_login("hod@demo.com", "password123")
    
    print("\n4. Testing Login with wrong credentials:")
    test_login("hod@demo.com", "wrongpassword")