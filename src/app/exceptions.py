from fastapi import HTTPException, status


class NotFoundError(HTTPException):
    def __init__(self, object_name):
        message = f"{object_name} not found"
        super().__init__(status.HTTP_404_NOT_FOUND, detail=message)


class JobNotFoundError(NotFoundError):
    def __init__(self, info):
        object_name = f"Job: {info}"
        super().__init__(object_name)


class EmployeeNotFoundError(NotFoundError):
    def __init__(self, info):
        object_name = f"Employee: {info}"
        super().__init__(object_name)


class EmployerNotFoundError(NotFoundError):
    def __init__(self, info):
        object_name = f"Employer: {info}"
        super().__init__(object_name)


class ApplyNotFoundError(NotFoundError):
    def __init__(self, info):
        object_name = f"Apply: {info}"
        super().__init__(object_name)


class AuthenError(HTTPException):
    def __init__(self, msg):
        if not msg:
            message = 'Access denied!!'
        else:
            message = msg
        super().__init__(status.HTTP_401_UNAUTHORIZED, detail=message)


class AuthorizationError(HTTPException):
    def __init__(self, message="Pemission denied!!"):
        super().__init__(status.HTTP_403_FORBIDDEN, detail=message)


class BadRequestsError(HTTPException):
    def __init__(self, message="Bad requests"):
        super().__init__(status.HTTP_400_BAD_REQUEST, detail=message)


AuthenticationError = AuthenError()
