
import re

def validate_email(email: str) -> bool:
    """Checks if email format is valid."""
    if not email:
        return False
    # Simple regex for email validation
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, email) is not None

def validate_phone(phone: str) -> bool:
    """Checks if phone contains at least 7 digits."""
    if not phone:
        return False
    digits = re.sub(r"\D", "", phone)
    return len(digits) >= 7

def validate_url(url: str) -> bool:
    """Basic URL validation."""
    if not url:
        return False
    # Allow simple domains or http/https
    # Check for at least one dot
    return "." in url and not " " in url
