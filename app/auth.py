from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import secrets

security = HTTPBearer()

# TODO: хранить сессии в базе. Пока так для простоты
sessions = {}


def create_session(user):
    session_token = secrets.token_urlsafe()
    sessions[session_token] = user
    return session_token


def get_session(credentials: HTTPAuthorizationCredentials = Depends(security)):
    session_token = credentials.credentials
    if session_token in sessions:
        return session_token
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid session token")


def remove_session(session_token):
    sessions.pop(session_token, None)
