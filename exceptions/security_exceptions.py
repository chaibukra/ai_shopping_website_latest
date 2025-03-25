from fastapi import HTTPException
from starlette import status


def user_credentials_exception() -> HTTPException:
    user_credentials_exception_response = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                                        detail="The username or password are incorrect")
    return user_credentials_exception_response


def token_exception() -> HTTPException:
    token_exception_response = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                             detail="The token provided is invalid")
    return token_exception_response


def username_taken_exception() -> HTTPException:
    username_taken_exception_response = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Provided username already taken"
    )
    return username_taken_exception_response


def user_unauthorized_exception() -> HTTPException:
    user_unauthorized_exception_response = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="You are not authorized to perform this action, Please login"
    )
    return user_unauthorized_exception_response


def delete_user_exception() -> HTTPException:
    delete_user_exception_response = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Can't delete this user, The username or password are incorrect"
    )
    return delete_user_exception_response
