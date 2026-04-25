from pydantic import BaseModel, EmailStr


class UserSchema(BaseModel):
    id: int
    username: str
    password: str
    email: EmailStr
    first_name: str
    last_name: str
    is_active: bool


class CredentialsSchema(BaseModel):
    username: str | None = None
    password: str
    email: EmailStr | None = None
