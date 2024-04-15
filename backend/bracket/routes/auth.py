from typing import Any

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

auth = init_auth("https://046425272.propelauthtest.com", "bbddd842b0cec6f0c787e97b915ce786495330bb6b3f8f8b838e5183ef2e8055ec776de721b94bd641b918acec523bb4")
