from fastapi import APIRouter, Depends, HTTPException, status
from models import User, LoginUser, CreateUser
from crud.users import create_user, get_user_by_id, verify_user
from dependencies import get_current_user
from auth import get_session, create_session, remove_session

router = APIRouter(prefix='/v1')


@router.post("/users/")
async def create_user_endpoint(user: CreateUser):
    user_id = await create_user(user)
    return {"user_id": user_id}


@router.post("/login/")
async def login(user: LoginUser):
    user = await verify_user(user.username, user.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    session_token = create_session(user)
    return {"session_token": session_token}


@router.get("/users/{user_id}")
async def get_user_data(user_id: str, current_user: User = Depends(get_current_user)):
    user = await get_user_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.post("/logout/")
async def logout(session_token: str = Depends(get_session)):
    remove_session(session_token)
    return {"message": "Logged out successfully"}
