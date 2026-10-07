from pydantic import BaseModel, Field


class TopicRequest(BaseModel):
    topic: str = Field(min_length=1, max_length=500)


class TextRequest(BaseModel):
    text: str = Field(min_length=1, max_length=30000)


class QuizQuestion(BaseModel):
    question: str
    options: list[str] = Field(min_length=4, max_length=4)
    answer: str


class QuizResponse(BaseModel):
    quiz: list[QuizQuestion]


class LearningResponse(BaseModel):
    topic: str
    recommendations: str
