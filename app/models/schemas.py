from typing import Optional, Generic, TypeVar
from pydantic import BaseModel , Field
from pydantic.generics import GenericModel

T = TypeVar('T')


class QuestionSchema(BaseModel):
    id: Optional[int] = None
    text: Optional[str] = None
    answer: Optional[str] = None
    created_at: Optional[str] = None

    class Config:
        orm_mode = True


class Request(GenericModel, Generic[T]):
    parameter: Optional[T] = Field(...)


class RequestQuestion(BaseModel):
    parameter: QuestionSchema = Field(...)


class Response(GenericModel, Generic[T]):
    code: str
    status: str
    message: str
    result: Optional[T]
