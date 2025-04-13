import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from contextlib import asynccontextmanager
from profile_endpoints import profile_router
from book_endpoints import book_router
from auth_endpoints import auth_router

from connection import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(auth_router)
app.include_router(profile_router)
app.include_router(book_router)

if __name__ == '__main__':
    uvicorn.run(app, host='localhost', port=8080, reload=True)
