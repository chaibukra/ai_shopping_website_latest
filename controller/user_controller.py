from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from starlette import status
from exceptions.security_exceptions import delete_user_exception, token_exception, user_unauthorized_exception
from model.user_request import UserRequest
from service import user_service, auth_service

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")

router = APIRouter(
    prefix="/user",
    tags=["user"],
    responses={401: {"user": "Not authorized"}}
)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(user_request: UserRequest):
    await user_service.create_user(user_request)


@router.delete("/", status_code=status.HTTP_200_OK)
async def delete_user(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await auth_service.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise delete_user_exception()
    await user_service.delete_user(user)


@router.get("/role", status_code=status.HTTP_200_OK)
async def get_user_role(token: str = Depends(oauth2_bearer)):
    user = await auth_service.token_get_user_role(token)
    if not user:
        raise token_exception()
    return {"role": user}


@router.get("/", status_code=status.HTTP_200_OK)
async def get_all_users(token: str = Depends(oauth2_bearer)):
    user = await auth_service.token_get_user_role(token)
    if not user:
        raise token_exception()
    if user != "admin":
        raise user_unauthorized_exception()

    return await user_service.get_all_users()
