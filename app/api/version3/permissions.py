from functools import wraps
from flask_jwt_extended import get_jwt_identity

from .models.users import ADMIN, UserManager


def admin_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        user_id = get_jwt_identity()
        manager = UserManager()
        user = manager.fetch_by_id(user_id)
        if user.role != ADMIN:
            payload = {
                "message": "Sorry, you are unauthorized",
            }
            return payload, 401
        return f(*args, **kwargs)
    return wrapper
