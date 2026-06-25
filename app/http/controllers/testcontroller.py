from app.http.request.test_request import TestRequest
from fastapi import APIRouter
router = APIRouter(tags=["Test Controller"])

@router.get("")
async def get_test(data: TestRequest):
    return{
        "status" : "ok"
    }