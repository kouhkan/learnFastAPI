from fastapi import HTTPException, status


class UserNotFoundException(HTTPException):
    def __init__(self):
        self.status_code = status.HTTP_404_NOT_FOUND
        self.detail = "User not found!"


class DuplicateUserException(HTTPException):
    def __init__(self):
        self.status_code = status.HTTP_409_CONFLICT
        self.detail = "This user is already registered!"


class WrongPasswordException(HTTPException):
    def __init__(self):
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.detail = "Wrong password!"


class ExpiredTokenException(HTTPException):
    def __init__(self):
        self.status_code = status.HTTP_401_UNAUTHORIZED
        self.detail = "Token has expired!"


class InvalidCredentialsException(HTTPException):
    def __init__(self):
        self.status_code = status.HTTP_403_FORBIDDEN
        self.detail = "Could not validate credentials."
        self.headers = {"WWW-Authenticate": "Bearer"}


class AuthenticationException(HTTPException):
    def __init__(self):
        self.status_code = status.HTTP_401_UNAUTHORIZED
        self.detail = "auth header not found."
