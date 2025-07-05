# utils/custom_exceptions.py
class AppError(Exception):
    def __init__(self, message="Application Error", status_code=500):
        self.message = message
        self.status_code = status_code
        super().__init__(message)
