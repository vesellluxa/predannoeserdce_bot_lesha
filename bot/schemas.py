from pydantic import BaseModel, ConfigDict, EmailStr, Field


class CreateUserDto(BaseModel):
    username: str = Field(..., min_length=5, max_length=32)
    email: str = EmailStr
    name: str = Field(..., min_length=1, max_length=64)
    surname: str = Field(..., min_length=1, max_length=64)
    phone: str = Field(pattern=r"^[0-9]+$", max_length=12)
    chat_id: int

    model_config = ConfigDict(regex_engine="python-re")


class QuestionDto(BaseModel):
    question: str = Field(..., min_lenght=5, max_lenght=256)
    username: str = Field(..., min_length=5, max_length=32)
    chat_id: int
