import datetime
from typing import Literal
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, field_validator, validate_email
from pydantic_core.core_schema import ValidationInfo


class PasswordMixin(BaseModel):
    password: str

    @staticmethod
    @field_validator('password')
    def check_password(cls, v: str) -> str:
        # TODO: accomplish more strict password validation
        if len(v) < 1:
            raise ValueError('password must has at list one character')

        return v


class LoginUser(PasswordMixin):
    username: str


class UserMixin(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    date_of_birth: datetime.date
    user_gender: Literal['муж', 'жен']
    city: str
    interests: str | None = Field(default=None)

    @staticmethod
    @field_validator('first_name', 'last_name')
    def check_alphabetic(cls, v: str, info: ValidationInfo) -> str:
        if isinstance(v, str):
            assert v, f'{info.field_name} cannot be empty'
            assert v.isalpha(), f'{info.field_name} must be alphabetic'
        return v

    @staticmethod
    @field_validator("user_email")
    def validate_email(cls, value):
        try:
            validate_email(value)
        except Exception:
            raise ValueError("Invalid email format")
        return value


class User(UserMixin):
    id: UUID = Field(default_factory=uuid4)


class CreateUser(UserMixin, PasswordMixin):
    pass
