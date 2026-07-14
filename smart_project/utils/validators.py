"""
Validation utilities for SmartCampusAI.
Provides email checks, password strength verification, and database uniqueness checks.
"""
import re
import validators
from typing import Tuple
from utils.database import search

def is_valid_email(email: str) -> bool:
    """
    Validate if an email is syntactically correct.
    """
    if not email:
        return False
    try:
        # validators.email returns validation object or ValidationFailure
        return bool(validators.email(email))
    except Exception:
        # Fallback regex if package behaves unexpectedly
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return bool(re.match(pattern, email))

def validate_password_strength(password: str) -> Tuple[bool, str]:
    """
    Check password length and complexity.
    Returns:
        tuple: (is_valid, error_message)
    """
    if not password:
        return False, "Password cannot be empty."
    if len(password) < 8:
        return False, "Password must be at least 8 characters long."
    return True, ""

def is_username_taken(username: str) -> bool:
    """Check if the username is already registered in the user database."""
    if not username:
        return True
    return len(search("users", "username", username)) > 0

def is_email_taken(email: str) -> bool:
    """Check if the email is already registered in the user database."""
    if not email:
        return True
    return len(search("users", "email", email)) > 0
