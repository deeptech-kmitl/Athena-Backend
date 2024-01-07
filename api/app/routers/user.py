from fastapi import APIRouter, Depends
from pydantic import BaseModel
from middleware.auth import get_auth_user, AuthDep

router = APIRouter(
    prefix="/user",
    tags=["User"],
    responses={404: {"message": "Not found"}},
    dependencies=[Depends(get_auth_user)],
)


@router.get("/profile")
def profile(auth: AuthDep):
    return {"message": "ok", "session": auth, "user": auth.user}
