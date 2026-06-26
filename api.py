from app.config.database import get_db
from fastapi import Depends
from app.http.controllers import testcontroller, airbnb_controller
from fastapi import FastAPI

def routing(app: FastAPI): 
    app.include_router(testcontroller.router, prefix="/test")
    
    app.include_router(airbnb_controller.router, prefix="/airbnb", dependencies=[Depends(get_db)])


    return app