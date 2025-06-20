from flask_jwt_extended import (
    create_access_token,
    get_jwt_identity,
    jwt_required as flask_jwt_required
)
from datetime import timedelta


class JWTManagerHelper:
    def __init__(self, expiry_days=1):
        self._expiry = timedelta(days=expiry_days)

    def generate_token(self, user_id):
        return create_access_token(identity=user_id, expires_delta=self._expiry)

    def get_user_id(self):
        return get_jwt_identity()

    @property
    def jwt_required(self):
        return flask_jwt_required

jwt_manager = JWTManagerHelper()
