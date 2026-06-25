from app.http.controllers import testcontroller
from fastapi import FastAPI

def routing(app: FastAPI): 
    app.include_router(testcontroller.router, prefix="/test")

    return app