from typing import Annotated
from fastapi import Cookie, HTTPException, status, Request, Depends
from database.engine import SessionLocal
import repository.session as sessionRepo
import jwt
from sqlalchemy.orm import Session

jwtSecret = "javainuse-awdawdawdawdawd-key"


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_auth_user(request: Request, db: Session = Depends(get_db)):
    """verify that user has a valid session"""
    session_id = request.cookies.get("sec")
    if not session_id:
        raise HTTPException(status_code=401)
    jwtJson = jwt.decode(session_id, jwtSecret, algorithms=["HS256"])
    if not jwtJson:
        raise HTTPException(status_code=401)
    session = sessionRepo.get_session(db, jwtJson["i"])
    if not session or session.is_revoke:
        raise HTTPException(status_code=403)
    return session


AuthDep = Annotated[dict, Depends(get_auth_user)]
