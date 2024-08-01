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


def user_to_dict(user: User) -> dict:
    return {
        "uid": user.uid,
        "username": user.username,
        "email": user.email,
        "display_name": user.display_name,
        "profile_picture_url": user.profile_picture_url,
        "reputation": user.reputation,
        "bio": user.bio,
    }