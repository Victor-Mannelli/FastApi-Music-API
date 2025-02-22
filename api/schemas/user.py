from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
  username: str
  email: str
  
class UserCreate(UserBase):
  password: str

class UserUpdate(UserBase):
  username: Optional[str] = None
  email: Optional[str] = None
  
class UserOut(UserBase):
    id: int

    class Config:
      from_attributes = True