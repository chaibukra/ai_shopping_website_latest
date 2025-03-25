from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer

from exceptions.security_exceptions import user_unauthorized_exception
from service import predict_service, auth_service

router = APIRouter(
    prefix="/predict",
    tags=["predict"],
)

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")


@router.get("/predict_user_expenses_for_tech_items")
async def predict_user_expenses_for_tech_items(user_id: int, token: str = Depends(oauth2_bearer)):
    role = await auth_service.token_get_user_role(token)
    if role != "admin":
        raise user_unauthorized_exception()
    prediction = await predict_service.predict_user_expenses_for_tech_items(user_id)
    return {"prediction": f"{prediction[0]:.2f} USD"}
