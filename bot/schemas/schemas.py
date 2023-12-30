from pydantic import BaseModel, ConfigDict, EmailStr, Field
import datetime


class CreateUserShortDto(BaseModel):
    username: str = Field(..., min_length=5, max_length=32)
    chat_id: int


class UpdateUser(CreateUserShortDto):
    email: EmailStr
    name: str = Field(..., min_length=1, max_length=64)
    second_name: str = Field(..., min_length=1, max_length=64)
    surname: str = Field(..., min_length=1, max_length=64)
    phone_number: str = Field(pattern=r"^[0-9]+$", max_length=12)
    chat_id: int

    model_config = ConfigDict(regex_engine="python-re")


class CreateQuestionDto(BaseModel):
    text: str = Field(..., min_length=1, max_length=256)
    owner: int


class QuestionSchema(BaseModel):
    text: str = Field(..., min_length=1, max_length=256)
    answer: str = Field(..., min_length=1, max_length=2500)


class InformationSchema(BaseModel):
    faq: dict[int, QuestionSchema]
    info: dict[int, QuestionSchema]
    needs: dict[int, QuestionSchema]
    donations: dict[int, QuestionSchema]
    list_animals: dict[int, QuestionSchema]


class UserSchemaShort(BaseModel):
    chat_id: int


class NewsletterSchema(BaseModel):
    id: int
    text: str = Field(..., min_length=1, max_length=2500)
    sending_date: datetime.datetime
    is_finished: bool
    users: list[UserSchemaShort]


class Question:
    """
    Represents a question with its corresponding answer.

    Attributes:
        text (str): The text of the question.
        answer (str): The answer to the question.
    """

    def __init__(self, text, answer):
        self.text = text
        self.answer = answer

    def __repr__(self):
        return f"{self.text}: {self.answer}"
