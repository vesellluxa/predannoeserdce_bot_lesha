from pydantic import BaseModel, ConfigDict, Field, EmailStr

class CreateUserDto(BaseModel):
    username: str = Field(..., min_length=5, max_length=32)
    email: str = EmailStr
    name: str = Field(..., min_length=1, max_length=64)
    surname: str = Field(..., min_length=1, max_length=64)
    phone: str = Field(pattern=r'^[0-9]+$', max_length=12)
    chat_id: str = Field(..., max_length=10)

    model_config = ConfigDict(regex_engine='python-re')
    

    