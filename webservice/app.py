from fastapi import FastAPI

from routes.enhanced import router as EnhancedRouter


app = FastAPI()

app.include_router(EnhancedRouter, tags=["Enhanced"], prefix="/enhanced")


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to this fantastic app!"}
