from fastapi import FastAPI, Depends, HTTPException
from contextlib import asynccontextmanager
from sqlmodel import select
from models.models import *
from models.public_models import ProfilePublic, BookPublic
from connection import init_db, get_session
from typing_extensions import TypedDict

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/profile_list", response_model=list[ProfilePublic])
def get_profile_list(session=Depends(get_session)):
    found = session.exec(select(Profile)).all()
    return found

@app.get("/profile/{id}", response_model=ProfilePublic)
def get_profile(profile_id: int, session=Depends(get_session)):
    profile = session.get(Profile, profile_id)
    if not profile:
        raise HTTPException(status_code=404, detail="profile not found")
    return profile

@app.post("/profile")
def create_profile(profile: ProfileDefault, session=Depends(get_session)) -> TypedDict('Response', {"status": int, "created": Profile}):
    profile = Profile.model_validate(profile)
    session.add(profile)
    session.commit()
    session.refresh(profile)
    return {"status": 201, "created": profile}


@app.delete("/profile/{id}")
def delete_profile(profile_id: int, session=Depends(get_session)) -> TypedDict('Response', {"status": int, "msg": str}):
    profile = session.get(Profile, profile_id)
    if not profile:
        raise HTTPException(status_code=404, detail="profile not found")
    return { "status": 204, "msg": "profile deleted" }


@app.patch("/profile/{id}")
def update_profile(profile_id: int, upd_profile: ProfileDefault, session=Depends(get_session)) -> TypedDict('Response', {"status": int, "updated": Profile}):
    profile = session.get(Profile, profile_id)
    if not profile:
        raise HTTPException(status_code=404, detail="profile not found")
    upd_data = upd_profile.model_dump(exclude_unset=True)
    for key, value in upd_data.items():
        setattr(profile, key, value)
    session.add(profile)
    session.commit()
    session.refresh(profile)
    return {"status": 202, "updated": profile}


@app.get("/book_instance/{id}", response_model=BookPublic)
def get_book_instance(book_id: int, session=Depends(get_session)):
    book = session.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="book not found")
    return book


@app.post("/book_instance")
def create_book_instance(new_book: BookDefault, session=Depends(get_session)) -> TypedDict('Response', {"status": int, "created": Book}):
    new_book = Book.model_validate(new_book)
    session.add(new_book)
    session.commit()
    session.refresh(new_book)
    return {"status": 201, "created": new_book}


@app.post("/book_info")
def create_book_instance(book: BookInfoDefault, session=Depends(get_session)) -> TypedDict('Response', {"status": int, "created": BookInfo}):
    book = BookInfo.model_validate(book)
    session.add(book)
    session.commit()
    session.refresh(book)
    return {"status": 201, "created": book}
