from fastapi import APIRouter, Depends

from bracket.logic.subscriptions import check_requirement
from bracket.models.db.club import ClubCreateBody, ClubUpdateBody
from bracket.models.db.user import UserPublic
from bracket.routes.auth import auth
from bracket.routes.models import ClubResponse, ClubsResponse, SuccessResponse
from bracket.routes.users import get_user_by_id
from bracket.sql.clubs import create_club, get_clubs_for_user_id, sql_delete_club, sql_update_club, sql_get_club_by_club_id
from bracket.utils.errors import ForeignKey, check_foreign_key_violation
from bracket.utils.id_types import ClubId
from bracket.utils.types import assert_some
from propelauth_fastapi import User as User_propelauth
from bracket.routes.users import register_user

router = APIRouter()

@router.get("/club", tags=["Clubs"], response_model=ClubResponse)
async def get_club_by_club_id(club_id: ClubId, user: User_propelauth = Depends(auth.require_user)) -> ClubsResponse:
    return ClubResponse(data=await sql_get_club_by_club_id(club_id))

@router.get("/clubs", tags=["Clubs"], response_model=ClubsResponse)
async def get_clubs(user: User_propelauth = Depends(auth.require_user)) -> ClubsResponse:
    return ClubsResponse(data=await get_clubs_for_user_id(assert_some(user.user_id)))


@router.post("/clubs", tags=["Clubs"], response_model=ClubResponse)
async def create_new_club(
    club: ClubCreateBody, user: User_propelauth = Depends(auth.require_user)) -> ClubResponse:
    
    user_id = user.user_id
    bracket_user = await get_user_by_id(assert_some(user_id))

        # If user does not have a bracket_id, create a bracket user
    if not bracket_user:
        bracket_user = await register_user(user_id)

    existing_clubs = await get_clubs_for_user_id(assert_some(user_id))
    check_requirement(existing_clubs, bracket_user, "max_clubs")
    return ClubResponse(data=await create_club(club, assert_some(user_id)))


@router.delete("/clubs/{club_id}", tags=["Clubs"], response_model=SuccessResponse)
async def delete_club(
    club_id: ClubId, _: User_propelauth = Depends(auth.require_user)
) -> SuccessResponse:
    with check_foreign_key_violation({ForeignKey.tournaments_club_id_fkey}):
        await sql_delete_club(club_id)

    return SuccessResponse()


@router.put("/clubs/{club_id}", tags=["Clubs"], response_model=ClubResponse)
async def update_club(
    club_id: ClubId, club: ClubUpdateBody, _: User_propelauth = Depends(auth.require_user)
) -> ClubResponse:
    return ClubResponse(data=await sql_update_club(club_id, club))
