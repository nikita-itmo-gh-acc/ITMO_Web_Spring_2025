from pydantic import BaseModel, Field
from datetime import date
from typing import Optional, List


class BookInfo(BaseModel):
    id: int
    title: str
    author: str
    release_date: date
    genre: str
    tags: Optional[List[str]] = Field(default_factory=list)


class Book(BaseModel):
    id: int
    info: BookInfo
    # owner: Profile
    own_since: date


class Profile(BaseModel):
    id: int
    name: str
    # description: str
    register_date: date
    birth_date: date
    books: Optional[List[Book]] = Field(default_factory=list)


class Tag(BaseModel):
    id: int
    name: str


class ShareRequest(BaseModel):
    id: int
    sender: Profile
    receiver: Profile
    suggested_book: Book
    received_book: Book
    status: str
    requested_date: date
