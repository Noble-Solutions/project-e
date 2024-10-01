from app import app
from api import router as api_router

app.include_router(api_router)


@app.get("/")
async def root():
    return {"message": "Hello world"}
