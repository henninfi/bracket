from typing import Any
from dotenv import load_dotenv
import os

import jwt
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from heliclockter import datetime_utc, timedelta
from jwt import DecodeError, ExpiredSignatureError
from pydantic import BaseModel
from starlette.requests import Request

from bracket.config import config
from bracket.database import database
from bracket.models.db.tournament import Tournament
from bracket.models.db.user import UserInDB, UserPublic
from bracket.schema import tournaments
from bracket.sql.tournaments import sql_get_tournament_by_endpoint_name
from bracket.sql.users import get_user, get_user_access_to_club, get_user_access_to_tournament
from bracket.utils.db import fetch_all_parsed
from bracket.utils.id_types import ClubId, TournamentId, UserId
from bracket.utils.security import verify_password
from bracket.utils.types import assert_some
from propelauth_fastapi import init_auth



router = APIRouter()

if os.getenv('ENVIRONMENT') == 'PRODUCTION':
    # Load environment variables from .env file
    load_dotenv('prod_backend.env')
# Load environment variables from .env file
else: 
    load_dotenv('dev_backend.env')

# Accessing variables
PROP_AUTH_URL = os.getenv('PROP_AUTH_URL')
PROP_AUTH_SECRET = os.getenv('PROP_AUTH_SECRET')

auth = init_auth(PROP_AUTH_URL, PROP_AUTH_SECRET)
