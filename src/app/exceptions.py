from fastapi import HTTPException, status

class NotFoundError(HTTPException):
    def __init__(self, object_name):
        message = f"{object_name} not found"
        super().__init__(status.HTTP_404_NOT_FOUND, detail=message)


class JobNotFoundError(NotFoundError):
    def __init__(self, info):
        object_name = f"Job: {info}"
        super().__init__(object_name)

