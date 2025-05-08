from pydantic import BaseModel

class ItemCreate(BaseModel):
    name: str
    last_name: str
    tel: str
    email: str

class ItemUpdate(BaseModel):
    name: str
    last_name: str
    tel: str
    email: str