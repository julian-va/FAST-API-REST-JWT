from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from src.controllers.auth_controller import routes_auth
from src.controllers.user_controller import routes_users
from src.databases.config_db import create_schemes

create_schemes()

app: FastAPI = FastAPI()
load_dotenv()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(routes_auth)
app.include_router(routes_users)
