from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from crud.contest_router import contest_router
from crud.photo_router import photo_router
from auth.router import auth_router

app = FastAPI(root_path='/api')
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

app.include_router(auth_router)
app.include_router(contest_router)
app.include_router(photo_router)
