from app import app
from api import router as api_router

app.include_router(api_router)


@app.get("/")
async def root():
    for route in app.routes:
        print(route.path)
    return {"message": "Hello world"}
