from beanie import Document
from typing import Optional


class User(Document):
    uid: str
    username: str
    email: str
    display_name: Optional[str] = None
    profile_picture_url: Optional[str] = None
    reputation: Optional[int] = 0
    bio: Optional[str] = None

    class Settings:
        collection = "users"
