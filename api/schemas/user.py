from pydantic import BaseModel  # Import BaseModel, the foundation for Pydantic models
from typing import Optional  # Import Optional for fields that may be None

# Base schema that defines common fields for the user
class UserBase(BaseModel):
    username: str  # Every user must have a username
    email: str  # Every user must have an email

# Schema used for creating a new user, extends UserBase
class UserCreate(UserBase):
    password: str  # Password is required when creating a user

# Schema used for updating user details
class UserUpdate(UserBase):
    username: Optional[str] = None  # Username can be updated but is optional
    email: Optional[str] = None  # Email can be updated but is optional

# This schema will be used for user authentication.
class UserLogin(BaseModel):
    email: str  # User must provide an email to log in
    password: str  # User must provide a password to log in

# Schema used for output when returning user data
class UserOut(UserBase):
    id: int  # User ID is required in the response

    class Config:
        from_attributes = True  # This allows Pydantic to read data from ORM models
