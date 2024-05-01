from fastapi import Depends, HTTPException, status
from auth import get_session, sessions
from models import User


def get_current_user(session_token: str = Depends(get_session)):

    user_data = sessions.get(session_token)

    if not user_data:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid session token")

    return User(**user_data)
