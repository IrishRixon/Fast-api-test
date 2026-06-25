from pydantic import BaseModel
class TestRequest(BaseModel):
    text: str