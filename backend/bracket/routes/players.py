from fastapi import APIRouter, Depends
from propelauth_fastapi import User as User_propelauth

from bracket.database import database
from bracket.logic.subscriptions import check_requirement
from bracket.models.db.player import Player, PlayerBody, PlayerMultiBody
from bracket.models.db.user import UserPublic
from bracket.routes.users import get_user_by_id
from bracket.routes.auth import auth
from bracket.routes.models import (
    PaginatedPlayers,
    PlayersResponse,
    SinglePlayerResponse,
    SuccessResponse,
)
from bracket.schema import players
from bracket.sql.players import (
    get_all_players_in_tournament,
    get_player_count,
    insert_player,
    sql_delete_player,
)
from bracket.utils.db import fetch_one_parsed
from bracket.utils.id_types import PlayerId, TournamentId
from bracket.utils.pagination import PaginationPlayers
from bracket.utils.types import assert_some

router = APIRouter()


@router.get("/tournaments/{tournament_id}/players", tags = ["players"], response_model=PlayersResponse)
async def get_players(
    tournament_id: TournamentId,
    not_in_team: bool = False,
    pagination: PaginationPlayers = Depends(),
    _: User_propelauth = Depends(auth.require_user),
) -> PlayersResponse:
    return PlayersResponse(
        data=PaginatedPlayers(
            players=await get_all_players_in_tournament(
                tournament_id, not_in_team=not_in_team, pagination=pagination
            ),
            count=await get_player_count(tournament_id, not_in_team=not_in_team),
        )
    )


@router.put("/tournaments/{tournament_id}/players/{player_id}", tags = ["players"], response_model=SinglePlayerResponse)
async def update_player_by_id(
    tournament_id: TournamentId,
    player_id: PlayerId,
    player_body: PlayerBody,
    _: User_propelauth = Depends(auth.require_user),
) -> SinglePlayerResponse:
    await database.execute(
        query=players.update().where(
            (players.c.id == player_id) & (players.c.tournament_id == tournament_id)
        ),
        values=player_body.model_dump(),
    )
    return SinglePlayerResponse(
        data=assert_some(
            await fetch_one_parsed(
                database,
                Player,
                players.select().where(
                    (players.c.id == player_id) & (players.c.tournament_id == tournament_id)
                ),
            )
        )
    )


@router.delete("/tournaments/{tournament_id}/players/{player_id}", tags = ["players"], response_model=SuccessResponse)
async def delete_player(
    tournament_id: TournamentId,
    player_id: PlayerId,
    _: User_propelauth = Depends(auth.require_user),
) -> SuccessResponse:
    await sql_delete_player(tournament_id, player_id)
    return SuccessResponse()


@router.post("/tournaments/{tournament_id}/players", tags = ["players"], response_model=SuccessResponse)
async def create_single_player(
    player_body: PlayerBody,
    tournament_id: TournamentId,
    user: User_propelauth = Depends(auth.require_user),
) -> SuccessResponse:
    public_user = await get_user_by_id(assert_some(user.properties['bracket_id']))
    existing_players = await get_all_players_in_tournament(tournament_id)
    check_requirement(existing_players, public_user, "max_players")
    await insert_player(player_body, tournament_id)
    return SuccessResponse()


@router.post("/tournaments/{tournament_id}/players_multi", tags = ["players"], response_model=SuccessResponse)
async def create_multiple_players(
    player_body: PlayerMultiBody,
    tournament_id: TournamentId,
    user: User_propelauth = Depends(auth.require_user),
) -> SuccessResponse:
    public_user = await get_user_by_id(assert_some(user.properties['bracket_id']))
    player_names = [player.strip() for player in player_body.names.split("\n") if len(player) > 0]
    existing_players = await get_all_players_in_tournament(tournament_id)
    check_requirement(existing_players, public_user, "max_players", additions=len(player_names))

    for player_name in player_names:
        await insert_player(PlayerBody(name=player_name, active=player_body.active), tournament_id)

    return SuccessResponse()
