from fastapi import APIRouter, HTTPException, Depends, Request
from sqlmodel import select
from models.models import *
from connection import get_session
from models.public_models import ProfilePublic
from auth_endpoints import auth_checker
from typing_extensions import TypedDict

profile_router = APIRouter()

@profile_router.get("/profile_list", response_model=list[ProfilePublic])
@auth_checker
async def get_profile_list(session=Depends(get_session)):
    found = session.exec(select(Profile)).all()
    return found

@profile_router.get("/profile/{id}", response_model=ProfilePublic)
async def get_profile(profile_id: int, session=Depends(get_session)):
    profile = session.get(Profile, profile_id)
    if not profile:
        raise HTTPException(status_code=404, detail="profile not found")
    return profile

@profile_router.post("/profile")
@auth_checker
async def create_profile(profile: ProfileDefault, session=Depends(get_session)) -> TypedDict('Response', {"status": int, "created": Profile}):
    profile = Profile.model_validate(profile)
    session.add(profile)
    session.commit()
    session.refresh(profile)
    return {"status": 201, "created": profile}


@profile_router.delete("/profile/{id}")
async def delete_profile(profile_id: int, session=Depends(get_session)) -> TypedDict('Response', {"status": int, "msg": str}):
    profile = session.get(Profile, profile_id)
    if not profile:
        raise HTTPException(status_code=404, detail="profile not found")
    return { "status": 204, "msg": "profile deleted" }


@profile_router.patch("/profile/{id}")
async def update_profile(profile_id: int, upd_profile: ProfileDefault, session=Depends(get_session)) -> TypedDict('Response', {"status": int, "updated": Profile}):
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
