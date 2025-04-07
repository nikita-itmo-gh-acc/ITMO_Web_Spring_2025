from fastapi import FastAPI
from mock import mock_db
from models import *
from typing import List
from typing_extensions import TypedDict

app = FastAPI()


@app.get("/")
def root():
    return {"ok": True}


@app.get("/profile_list")
def profile_list() -> List[Profile]:
    return mock_db


@app.get("/profile/{profile_id}")
def profile_get(profile_id: int) -> List[Profile]:
    return [p for p in mock_db if p.get("id") == profile_id]


@app.post("/profile")
def profile_create(profile: Profile) -> TypedDict('Response', {"status": int, "data": Profile}):
    new_profile = profile.model_dump()
    mock_db.append(new_profile)
    return {
        "status": 201,
        "data": profile
    }


@app.delete("profile/{profile_id}")
def profile_delete(profile_id: int) -> TypedDict('Response', {"status": int, "message": str}):
    for i, profile in enumerate(mock_db):
        if profile.get("id") == profile_id:
            mock_db.pop(i)
            break
    return {
        "status": 202,
        "message": "deleted"
    }


@app.put("/profile/{profile_id}")
def profile_update(profile_id: int, upd_profile: Profile) -> TypedDict('Response', {"status": int, "data": Profile}):
    for p in mock_db:
        if p.get("id") == profile_id:
            warrior_to_append = upd_profile.model_dump()
            mock_db.remove(p)
            mock_db.append(warrior_to_append)
    return {
        "status": 205,
        "data": upd_profile
    }
