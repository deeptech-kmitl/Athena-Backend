import base64
import hashlib
from fastapi import APIRouter, Depends, HTTPException, Header, Request
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
from uuid import uuid4

from typing import Annotated

from dotenv import dotenv_values

config = dotenv_values(".env")

router = APIRouter(
    prefix="/auth", tags=["Auth"], responses={404: {"message": "Not found"}}
)

CALLBACK_ENDPOINT = config["CALLBACK_ENDPOINT"]
JWT_SECRET = config["JWT_KEY"]

CLIENT_SECRETS_FILE = "client_secrets.json"
SCOPES = [
    "openid",
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
]

flow = Flow.from_client_secrets_file(
    CLIENT_SECRETS_FILE,
    scopes=SCOPES,
    redirect_uri=CALLBACK_ENDPOINT + "/auth/login/google/callback",
)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/login/google")
async def login(request: Request, back_to: str = ""):
    url, state = flow.authorization_url(include_granted_scopes="true")
    request.session["state"] = state
    request.session["back_to"] = back_to
    return RedirectResponse(url)


@router.get("/login/google/callback")
async def callback(
    request: Request,
    state: str,
    db: Session = Depends(get_db),
    user_agent: Annotated[str | None, Header()] = "",
):
    authorization_response = str(request.url)

    if not request.session.get("state") == state:
        raise HTTPException(400, "State does not match!")

    flow.fetch_token(authorization_response=authorization_response)

    # Optionally, view the email address of the authenticated user.
    user_info_service = build("oauth2", "v2", credentials=flow.credentials)
    user_info = user_info_service.userinfo().get().execute()

    email = user_info["email"]

    user = userRepo.get_user_by_email(db, email)
    if user == None:
        user = userRepo.create_user(db, schemas.UserCreate(email=email))

    session = sessionRepo.create_session(
        db,
        schemas.SessionCreate(
            user_id=user.id,
            user_agent=user_agent,
        ),
    )

    encoded_jwt = jwt.encode({"i": session.id}, JWT_SECRET, algorithm="HS256")

    response = RedirectResponse("/user/profile")
    back_to_b64_str = request.session.get("back_to")
    if not back_to_b64_str == "":
        try:
            response = RedirectResponse(
                base64.b64decode(back_to_b64_str).decode("ascii")
            )
        except:
            print("An exception occurred bad base64 back to")
    response.set_cookie(key="sec", value=encoded_jwt, httponly=True)
    return response


@router.get("/logout", dependencies=[Depends(get_auth_user)])
async def logout(response: Response):
    response.delete_cookie("sec")
    return {"message": "ok"}
