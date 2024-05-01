from fastapi import FastAPI

from api.v1 import users

app = FastAPI()

app.include_router(users.router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
