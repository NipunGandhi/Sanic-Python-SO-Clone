from beanie import init_beanie, Document
from typing import List, Optional
from motor.motor_asyncio import AsyncIOMotorClient
from models.user_model import User


class Sequence(Document):
    name: str
    sequence_value: int

    class Settings:
        collection = "sequences"


class Question(Document):
    title: str
    body: str
    user_id: str
    tags: List[str] = []
    score: Optional[int] = 0
    views: Optional[int] = 0
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    status: Optional[str] = 'open'

    class Settings:
        collection = "questions"


class Answer(Document):
    answer_id: str
    question_id: str
    user_id: str
    body: str
    score: Optional[int] = 0
    is_accepted: Optional[bool] = False
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    class Settings:
        collection = "answers"


class Comment(Document):
    user_id: str
    post_id: str
    body: str
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    class Settings:
        collection = "comments"


class Article(Document):
    article_id: str
    title: str
    body: str
    user_id: str
    tags: List[str] = []
    score: Optional[int] = 0
    views: Optional[int] = 0
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    class Settings:
        collection = "articles"


document_models = [User, Question, Answer, Comment, Article, Sequence]


async def init_db():
    uri = "mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+2.2.12"

    client = AsyncIOMotorClient(uri)
    database = client['temp']

    await init_beanie(database, document_models=document_models)

    try:
        client.admin.command('ping')
        print("Successfully connected to MongoDB!")

    except Exception as e:
        print(e)
