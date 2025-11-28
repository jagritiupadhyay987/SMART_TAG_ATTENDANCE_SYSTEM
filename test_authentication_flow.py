import requests
import json
from datetime import datetime
import jwt
import time

# Configuration
BASE_URL = "http://localhost:8000"
TIMEOUT = 30

# Test credentials
DEMO_CREDENTIALS = [
    {"email": "hod@demo.com", "password": "password123", "role": "hod"},
    {"email": "student@demo.com", "password": "password123", "role": "student"}
]

TEST_CREDENTIALS = [
    {"email": "hod_user@test.com", "password": "hod_password", "role": "hod"},
    {"email": "student_user@test.com", "password": "student_password", "role": "student"},
    {"email": "staff_user@test.com", "password": "staff_password", "role": "staff"}
]

# ANSI color codes for terminal output
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"
BOLD = "\033[1m"

def print_header(text):
    """Print a formatted header"""
    print(f"\n{BOLD}{BLUE}{'=' * 60}{RESET}")
    print(f"{BOLD}{BLUE}{text.center(60)}{RESET}")
    print(f"{BOLD}{BLUE}{'=' * 60}{RESET}\n")

def print_success(text):
    """Print a success message"""
    print(f"{GREEN}✓ {text}{RESET}")

def print_error(text):
    """Print an error message"""
    print(f"{RED}✗ {text}{RESET}")

def print_warning(text):
    """Print a warning message"""
    print(f"{YELLOW}! {text}{RESET}")

def print_info(text):
    """Print an info message"""
    print(f"{BLUE}ℹ {text}{RESET}")

def check_backend_health():
    """Check if backend is running and healthy"""
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=TIMEOUT)
        if response.status_code == 200:
            data = response.json()
            if data.get("database") == "connected" and data.get("status") in ("ok", "healthy"):
                print_success("Backend is running and healthy")
                return True
            else:
                print_warning(f"Backend is running but reports issues: {data}")
                return False
        else:
            print_error(f"Backend health check failed with status code: {response.status_code}")
            return False
    except requests.RequestException as e:
        print_error(f"Backend connection failed: {str(e)}")
        return False

def get_auth_token(email, password):
    """Get authentication token for a user"""
    url = f"{BASE_URL}/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {"username": email, "password": password}
    
    try:
        response = requests.post(url, headers=headers, data=data, timeout=TIMEOUT)
        if response.status_code == 200:
            token_data = response.json()
            return token_data.get("access_token")
        else:
            print_error(f"Authentication failed for {email}: {response.status_code}")
            try:
                print_error(f"Error details: {response.json()}")
            except:
                pass
            return None
    except requests.RequestException as e:
        print_error(f"Authentication request failed for {email}: {str(e)}")
        return None

def decode_token(token):
    """Decode JWT token without verification to inspect payload"""
    try:
        # Decode without verification - just to see the contents
        decoded = jwt.decode(token, options={"verify_signature": False}, algorithms=["HS256"])
        return decoded
    except Exception as e:
        print_error(f"Failed to decode token: {str(e)}")
        return None

def test_protected_endpoint(endpoint, method, token, data=None):
    """Test access to a protected endpoint"""
    url = f"{BASE_URL}{endpoint}"
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        if method.upper() == "GET":
            response = requests.get(url, headers=headers, timeout=TIMEOUT)
        elif method.upper() == "POST":
            if data:
                response = requests.post(url, headers=headers, json=data, timeout=TIMEOUT)
            else:
                response = requests.post(url, headers=headers, timeout=TIMEOUT)
        else:
            print_error(f"Unsupported method: {method}")
            return False
        
        if response.status_code == 200:
            return True
        else:
            print_warning(f"Endpoint {endpoint} returned status code: {response.status_code}")
            try:
                print_warning(f"Response: {response.json()}")
            except:
                print_warning(f"Response: {response.text[:100]}...")
            return False
    except requests.RequestException as e:
        print_error(f"Request to {endpoint} failed: {str(e)}")
        return False

def main():
    print_header("Authentication Flow Test")
    
    # Step 1: Check if backend is running
    if not check_backend_health():
        print_error("Backend health check failed. Please make sure the backend is running.")
        return
    
    # Step 2: Test authentication with demo credentials
    print_header("Testing Demo Credentials")
    demo_tokens = {}
    
    for cred in DEMO_CREDENTIALS:
        print_info(f"Testing login with {cred['email']} (role: {cred['role']})")
        token = get_auth_token(cred['email'], cred['password'])
        
        if token:
            print_success(f"Authentication successful for {cred['email']}")
            # Store tokens keyed by email instead of role to avoid collisions
            demo_tokens[cred['email']] = token
            
            # Decode and inspect token
            decoded = decode_token(token)
            if decoded:
                print_info(f"Token payload: {json.dumps(decoded, indent=2)}")
                
                # Verify user type in token
                if decoded.get("user_type") == cred['role']:
                    print_success(f"Token contains correct user type: {cred['role']}")
                else:
                    print_error(f"Token has incorrect user type: {decoded.get('user_type')} (expected: {cred['role']})")
                
                # Check token expiration
                if "exp" in decoded:
                    exp_time = datetime.fromtimestamp(decoded["exp"])
                    now = datetime.now()
                    if exp_time > now:
                        print_success(f"Token expiration valid: {exp_time}")
                    else:
                        print_error(f"Token already expired: {exp_time}")
                else:
                    print_error("Token missing expiration time")
        else:
            print_error(f"Authentication failed for {cred['email']}")
    
    # Step 3: Test authentication with test credentials
    print_header("Testing Test Credentials")
    test_tokens = {}
    
    for cred in TEST_CREDENTIALS:
        print_info(f"Testing login with {cred['email']} (role: {cred['role']})")
        token = get_auth_token(cred['email'], cred['password'])
        
        if token:
            print_success(f"Authentication successful for {cred['email']}")
            # Store tokens keyed by email instead of role to avoid collisions
            test_tokens[cred['email']] = token
            
            # Decode and inspect token
            decoded = decode_token(token)
            if decoded:
                print_info(f"Token payload: {json.dumps(decoded, indent=2)}")
                
                # Verify user type in token
                if decoded.get("user_type") == cred['role']:
                    print_success(f"Token contains correct user type: {cred['role']}")
                else:
                    print_error(f"Token has incorrect user type: {decoded.get('user_type')} (expected: {cred['role']})")
        else:
            print_error(f"Authentication failed for {cred['email']}")
    
    # Step 4: Test protected endpoints with valid tokens
    print_header("Testing Protected Endpoints")
    
    # Define test cases for protected endpoints with email and role
    test_cases = [
        # (endpoint, method, email, description)
        ("/students/", "GET", "hod@demo.com", "Get all students (HOD)"),
        ("/students/", "GET", "staff_user@test.com", "Get all students (Staff)"),
        ("/staff_dashboard/10-A", "GET", "staff_user@test.com", "Staff dashboard"),
        ("/hod_dashboard/10-A", "GET", "hod_user@test.com", "HOD dashboard"),
    ]
    
    # Add student-specific test cases
    for email in ["student@demo.com", "student_user@test.com"]:
        if email in demo_tokens or email in test_tokens:
            token = demo_tokens.get(email) or test_tokens.get(email)
            decoded = decode_token(token)
            if decoded and "admission_no" in decoded:
                admission_no = decoded["admission_no"]
                test_cases.append((f"/view_attendance/{admission_no}", "GET", email, f"View attendance (Student: {admission_no})"))
            else:
                print_warning(f"Student token for {email} missing admission_no claim, using default")
                test_cases.append((f"/view_attendance/ADM123", "GET", email, "View attendance (Student: default)"))
    
    # Run the test cases
    for endpoint, method, email, description in test_cases:
        tokens_dict = demo_tokens if email in demo_tokens else test_tokens
        if email in tokens_dict:
            print_info(f"Testing {description} with token for {email}")
            if test_protected_endpoint(endpoint, method, tokens_dict[email]):
                print_success(f"Access to {endpoint} successful with token for {email}")
            else:
                print_error(f"Access to {endpoint} failed with token for {email}")
        else:
            print_warning(f"Skipping {description} - no token available for {email}")
    
    # Step 5: Test token expiration (simulate by waiting)
    print_header("Testing Token Expiration (Simulated)")
    print_info("Note: This test simulates token expiration by decoding the token")
    print_info("In a real scenario, you would wait for the token to expire")
    
    # Get a sample token
    all_tokens = {}
    all_tokens.update(demo_tokens)
    all_tokens.update(test_tokens)
    sample_token = next(iter(all_tokens.values()), None)
    if sample_token:
        decoded = decode_token(sample_token)
        if decoded and "exp" in decoded:
            exp_time = datetime.fromtimestamp(decoded["exp"])
            now = datetime.now()
            time_to_expire = (exp_time - now).total_seconds()
            
            print_info(f"Token expires in {time_to_expire:.1f} seconds")
            print_info(f"Expiration time: {exp_time}")
            
            # Simulate what happens after expiration
            print_info("After expiration, the token would be rejected with a 401 Unauthorized error")
        else:
            print_error("Could not determine token expiration")
    else:
        print_error("No token available to test expiration")
    
    print_header("Authentication Test Summary")
    
    # Summarize demo credentials
    print_info("Demo Credentials:")
    for cred in DEMO_CREDENTIALS:
        status = "✓" if cred['email'] in demo_tokens else "✗"
        print(f"  {status} {cred['email']} ({cred['role']})")
    
    # Summarize test credentials
    print_info("Test Credentials:")
    for cred in TEST_CREDENTIALS:
        status = "✓" if cred['email'] in test_tokens else "✗"
        print(f"  {status} {cred['email']} ({cred['role']})")
    
    # Overall result
    if demo_tokens and test_tokens:
        print_success("Authentication system is working correctly with both demo and test credentials")
    elif demo_tokens:
        print_warning("Authentication works with demo credentials but not with test credentials")
    elif test_tokens:
        print_warning("Authentication works with test credentials but not with demo credentials")
    else:
        print_error("Authentication failed for all credentials")

if __name__ == "__main__":
    main()