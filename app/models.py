from pydantic import BaseModel, EmailStr

class UserRegister(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone_no: str

class QRData(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone_no: str
