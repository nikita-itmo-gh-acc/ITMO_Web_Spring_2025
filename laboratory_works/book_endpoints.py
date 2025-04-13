from fastapi import APIRouter, HTTPException, Depends
from models.models import *
from models.public_models import BookPublic
from connection import get_session
from typing_extensions import TypedDict

book_router = APIRouter()

@book_router.get("/book_instance/{id}", response_model=BookPublic)
def get_book_instance(book_id: int, session=Depends(get_session)):
    book = session.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="book not found")
    return book


@book_router.post("/book_instance")
def create_book_instance(new_book: BookDefault, session=Depends(get_session)) -> TypedDict('Response', {"status": int, "created": Book}):
    new_book = Book.model_validate(new_book)
    session.add(new_book)
    session.commit()
    session.refresh(new_book)
    return {"status": 201, "created": new_book}


@book_router.post("/book_info")
def create_book_instance(book: BookInfoDefault, session=Depends(get_session)) -> TypedDict('Response', {"status": int, "created": BookInfo}):
    book = BookInfo.model_validate(book)
    session.add(book)
    session.commit()
    session.refresh(book)
    return {"status": 201, "created": book}
