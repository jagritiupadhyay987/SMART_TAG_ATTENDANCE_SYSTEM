#!/usr/bin/env python3
"""
Test script to verify authentication fixes
"""

import requests
import json

# Test configuration
BASE_URL = "http://localhost:8000"
TEST_USERS = {
    "staff": {"email": "staff_user@test.com", "password": "staff_password"},
    "hod": {"email": "hod_user@test.com", "password": "hod_password"},
    "student": {"email": "student_user@test.com", "password": "student_password"}
}

def get_auth_token(email, password):
    """Get JWT token for user"""
    try:
        response = requests.post(f"{BASE_URL}/token", data={
            "username": email,
            "password": password
        })
        if response.status_code == 200:
            return response.json()["access_token"]
        else:
            print(f"❌ Auth failed for {email}: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"❌ Error getting token for {email}: {e}")
        return None

def test_endpoint(endpoint, method="GET", token=None, data=None, params=None):
    """Test an endpoint with authentication"""
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    
    try:
        if method == "GET":
            response = requests.get(f"{BASE_URL}{endpoint}", headers=headers, params=params)
        elif method == "POST":
            response = requests.post(f"{BASE_URL}{endpoint}", headers=headers, json=data)
        
        return response.status_code, response.text
    except Exception as e:
        return None, str(e)

def main():
    print("🧪 Testing Authentication Fixes")
    print("=" * 50)
    
    # Test 1: Get tokens for all users
    print("\n1️⃣ Testing JWT Token Generation")
    tokens = {}
    for role, creds in TEST_USERS.items():
        token = get_auth_token(creds["email"], creds["password"])
        if token:
            tokens[role] = token
            print(f"✅ {role.capitalize()} token: {token[:20]}...")
        else:
            print(f"❌ {role.capitalize()} token: FAILED")
    
    if not tokens:
        print("❌ No tokens obtained. Check server and user credentials.")
        return
    
    # Test 2: Test protected endpoints
    print("\n2️⃣ Testing Protected Endpoints")
    
    test_cases = [
        # (endpoint, method, required_role, description)
        ("/auto_attendance?admission_no=ADM001", "POST", "staff", "Auto Attendance"),
        ("/manual_attendance", "POST", "staff", "Manual Attendance"),
        ("/view_attendance/ADM001", "GET", "student", "View Attendance"),
        ("/staff_dashboard/10-A", "GET", "staff", "Staff Dashboard"),
        ("/hod_dashboard/10-A", "GET", "hod", "HOD Dashboard"),
        ("/staff_actions/ADM001", "GET", "staff", "Staff Actions"),
    ]
    
    for endpoint, method, required_role, description in test_cases:
        print(f"\n🔍 Testing {description}")
        
        if required_role not in tokens:
            print(f"❌ No token for {required_role}")
            continue
            
        token = tokens[required_role]
        
        # Prepare test data for POST requests
        data = None
        if method == "POST":
            if "manual_attendance" in endpoint:
                data = {
                    "admission_no": "ADM001",
                    "date": "2025-09-20",
                    "session": "morning",
                    "status": "Present"
                }
        
        status_code, response_text = test_endpoint(endpoint, method, token, data)
        
        if status_code == 200:
            print(f"✅ {description}: PASSED")
        elif status_code == 401:
            print(f"❌ {description}: 401 Unauthorized - Auth still broken")
        elif status_code == 403:
            print(f"⚠️ {description}: 403 Forbidden - Auth working, but permission issue")
        elif status_code == 404:
            print(f"⚠️ {description}: 404 Not Found - Auth working, but resource not found")
        else:
            print(f"❓ {description}: {status_code} - {response_text[:100]}...")
    
    # Test 3: Test without authentication (should fail)
    print("\n3️⃣ Testing Without Authentication (Should Fail)")
    status_code, _ = test_endpoint("/staff_dashboard/10-A", "GET")
    if status_code == 401:
        print("✅ Unauthenticated access properly blocked")
    else:
        print(f"❌ Unauthenticated access not blocked: {status_code}")
    
    print("\n" + "=" * 50)
    print("🏁 Authentication Test Complete")

if __name__ == "__main__":
    main()
