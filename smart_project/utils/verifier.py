"""
Verification script for SmartCampusAI.
Performs automated checks on imports, database structures, and security helper functions.
"""
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def verify_all():
    print("=== SmartCampusAI System Verification ===")
    
    # 1. Test imports
    try:
        from utils.database import load_json, search, insert, update
        from utils.security import hash_password, verify_password
        from utils.validators import is_valid_email, validate_password_strength
        from utils.config import get_gemini_api_key
        print("[OK] Core utilities imported successfully.")
    except Exception as e:
        print(f"[ERROR] Core utilities import failed: {e}")
        return False

    # 2. Test database seed records
    try:
        users = load_json("users")
        students = load_json("students")
        faculty = load_json("faculty")
        
        print(f"[OK] Users Table: Found {len(users)} records.")
        print(f"[OK] Students Table: Found {len(students)} records.")
        print(f"[OK] Faculty Table: Found {len(faculty)} records.")
        
        # Verify admin user exists
        admin_users = search("users", "username", "admin")
        if admin_users:
            print("[OK] Database search: Admin user located.")
        else:
            print("[ERROR] Database search: Admin user missing!")
            return False
    except Exception as e:
        print(f"[ERROR] Database load/search failed: {e}")
        return False
        
    # 3. Test Security Hashing
    try:
        test_pw = "mysecret123"
        hashed = hash_password(test_pw)
        if verify_password(test_pw, hashed):
            print("[OK] Security hashing and verification validated.")
        else:
            print("[ERROR] Security hashing verification failed!")
            return False
    except Exception as e:
        print(f"[ERROR] Security hashing failed: {e}")
        return False
        
    # 4. Test Validators
    try:
        assert is_valid_email("admin@university.edu") is True
        assert is_valid_email("invalid-email") is False
        
        is_pass, _ = validate_password_strength("short")
        assert is_pass is False
        is_pass, _ = validate_password_strength("longpassword123")
        assert is_pass is True
        
        print("[OK] Input validators validated.")
    except AssertionError:
        print("[ERROR] Validators assert check failed!")
        return False
    except Exception as e:
        print(f"[ERROR] Validators failed: {e}")
        return False
        
    # 5. Check environmental configs
    try:
        api_key = get_gemini_api_key()
        if api_key:
            print(f"[INFO] Gemini API key configuration: Found (first 4 chars: {api_key[:4]}...)")
        else:
            print("[INFO] Gemini API key configuration: Not Found (Offline Mode fallback will apply).")
        print("[OK] Environment configuration successfully read.")
    except Exception as e:
        print(f"[ERROR] Config read failed: {e}")
        return False

    print("\n[SUCCESS] ALL core system modules verified successfully! No errors detected.")
    return True

if __name__ == "__main__":
    success = verify_all()
    sys.exit(0 if success else 1)
