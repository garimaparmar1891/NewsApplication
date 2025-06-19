from flask_jwt_extended import (
    create_access_token,
    get_jwt_identity,
    jwt_required as flask_jwt_required
)
from datetime import timedelta

class JWTManagerHelper:
    def __init__(self, expiry_days=1):
        self.expiry = timedelta(days=expiry_days)

    def generate_token(self, user_id: int) -> str:
        """Generate a JWT token for the given user ID."""
        return create_access_token(identity=user_id, expires_delta=self.expiry)

    def get_user_id(self) -> int:
        """Extract user ID from JWT token."""
        return get_jwt_identity()

    @property
    def jwt_required(self):
        """Expose the Flask JWT-required decorator."""
        return flask_jwt_required

jwt_manager = JWTManagerHelper()
