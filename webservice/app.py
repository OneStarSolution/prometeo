from fastapi import FastAPI

from routes.enhanced import router as EnhancedRouter
from routes.redistribution import router as RedistributionRouter


app = FastAPI()

app.include_router(EnhancedRouter, tags=["Enhanced"], prefix="/enhanced")
app.include_router(RedistributionRouter, tags=[
                   "Redistribution"], prefix="/redistribution")


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to this fantastic app!"}
