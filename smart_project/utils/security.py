"""
Security utilities for SmartCampusAI.
Provides SHA-256 password hashing and validation.
"""
import hashlib

def hash_password(password: str) -> str:
    """
    Hash a password using SHA-256.
    
    Args:
        password (str): The plain-text password.
        
    Returns:
        str: The hex digest of the hashed password.
    """
    if not password:
        return ""
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def verify_password(password: str, hashed_password: str) -> bool:
    """
    Verify if a plain-text password matches a hash.
    
    Args:
        password (str): The plain-text password.
        hashed_password (str): The expected hashed password.
        
    Returns:
        bool: True if they match, else False.
    """
    return hash_password(password) == hashed_password
