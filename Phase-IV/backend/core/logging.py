import logging
from datetime import datetime
import json

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def log_auth_event(event_type: str, user_id: str = None, ip_address: str = None, details: dict = None):
    """
    Log authentication-related events.
    """
    event_data = {
        "timestamp": datetime.utcnow().isoformat(),
        "event_type": event_type,
        "user_id": user_id,
        "ip_address": ip_address,
        "details": details
    }

    logger.info(json.dumps(event_data))

def log_successful_login(user_id: str, ip_address: str = None):
    """Log successful login event."""
    log_auth_event("successful_login", user_id, ip_address)

def log_failed_login(email: str, ip_address: str = None):
    """Log failed login attempt."""
    log_auth_event("failed_login", details={"email": email}, ip_address=ip_address)

def log_registration_success(user_id: str, email: str, ip_address: str = None):
    """Log successful user registration."""
    log_auth_event("registration_success", user_id, ip_address, {"email": email})

def log_unauthorized_access(path: str, user_id: str = None, ip_address: str = None):
    """Log unauthorized access attempts."""
    log_auth_event("unauthorized_access", user_id, ip_address, {"path": path})