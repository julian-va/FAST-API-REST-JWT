from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from src.libs.utilities import Utilities
from src.controllers.auth_controller import routes_auth
from src.controllers.user_controller import routes_users
from src.controllers.files_controller import routes_files
from src.databases.config_db import create_schemes


app: FastAPI = FastAPI()
load_dotenv()
create_schemes()
Utilities.create_folders()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],

)
app.include_router(routes_auth)
app.include_router(routes_users)
app.include_router(routes_files)
