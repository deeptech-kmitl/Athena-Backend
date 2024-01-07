from fastapi import APIRouter, Depends, Header
from fastapi.responses import RedirectResponse, Response
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
import repository.session as sessionRepo
import repository.user as userRepo
from database.engine import SessionLocal
from sqlalchemy.orm import Session
import jwt
import schemas.user as schemas
from middleware.auth import get_auth_user
import os

from typing import Annotated

from dotenv import dotenv_values

config = dotenv_values(".env")

router = APIRouter(
    prefix="/auth", tags=["Auth"], responses={404: {"message": "Not found"}}
)

callbackEndpoint = config["CALLBACK_ENDPOINT"]
jwtSecret = config["JWT_KEY"]

flow = Flow.from_client_secrets_file(
    "./client_secrets.json",
    scopes=[
        "openid",
        "https://www.googleapis.com/auth/userinfo.email",
        "https://www.googleapis.com/auth/userinfo.profile",
    ],
    redirect_uri=callbackEndpoint + "/auth/login/google/callback",
)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/login/google")
async def login():
    auth_uri = flow.authorization_url()
    return RedirectResponse(auth_uri[0])


@router.get("/login/google/callback")
async def callback(
    code: str,
    db: Session = Depends(get_db),
    user_agent: Annotated[str | None, Header()] = "",
):
    flow.fetch_token(code=code)
    credentials = flow.credentials

    # Optionally, view the email address of the authenticated user.
    user_info_service = build("oauth2", "v2", credentials=credentials)
    user_info = user_info_service.userinfo().get().execute()

    email = user_info["email"]

    user = userRepo.get_user_by_email(db, email)
    if user == None:
        user = userRepo.create_user(db, schemas.UserCreate(email=email))

    session = sessionRepo.create_session(
        db, schemas.SessionCreate(user_id=user.id, user_agent=user_agent)
    )

    encoded_jwt = jwt.encode({"i": session.id}, jwtSecret, algorithm="HS256")

    response = RedirectResponse("/user/profile")
    response.set_cookie(key="sec", value=encoded_jwt)
    return response


@router.get("/logout", dependencies=[Depends(get_auth_user)])
async def logout(response: Response):
    response.delete_cookie("sec")
    return {"message": "ok"}
