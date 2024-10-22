class NotFoundError(Exception):
    def __init__(self, message="Resource not found", status_code=404):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

class BadRequestError(Exception):
    def __init__(self, message="Bad request", status_code=400):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

class ForbiddenError(Exception):
    def __init__(self, message="Access denied", status_code=403):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

class UnauthorizedError(Exception):
    def __init__(self, message="Unauthorized", status_code=401):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

class InternalServerError(Exception):
    def __init__(self, message="An internal error occurred", status_code=500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)
