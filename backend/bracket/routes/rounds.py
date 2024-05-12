from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from propelauth_fastapi import User as User_propelauth

from bracket.database import database
from bracket.logic.ranking.elo import recalculate_ranking_for_tournament_id
from bracket.logic.subscriptions import check_requirement
from bracket.models.db.round import (
    Round,
    RoundCreateBody,
    RoundToInsert,
    RoundUpdateBody,
)
from bracket.models.db.user import UserPublic
from bracket.models.db.util import RoundWithMatches
from bracket.routes.auth import auth
from bracket.routes.models import SuccessResponse
from bracket.routes.users import get_user_by_id
from bracket.routes.util import (
    round_dependency,
    round_with_matches_dependency,
)
from bracket.schema import rounds
from bracket.sql.rounds import get_next_round_name, set_round_active_or_draft, sql_create_round
from bracket.sql.stage_items import get_stage_item
from bracket.sql.stages import get_full_tournament_details
from bracket.sql.validation import check_foreign_keys_belong_to_tournament
from bracket.utils.id_types import RoundId, TournamentId
from bracket.utils.types import assert_some


router = APIRouter()


@router.delete("/tournaments/{tournament_id}/rounds/{round_id}", tags = ["Rounds"], response_model=SuccessResponse)
async def delete_round(
    tournament_id: TournamentId,
    round_id: RoundId,
    _: User_propelauth = Depends(auth.require_user),
    round_with_matches: RoundWithMatches = Depends(round_with_matches_dependency),
) -> SuccessResponse:
    if len(round_with_matches.matches) > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Round contains matches, delete those first",
        )

    await database.execute(
        query=rounds.delete().where(
            rounds.c.id == round_id and rounds.c.tournament_id == tournament_id
        ),
    )
    await recalculate_ranking_for_tournament_id(tournament_id)
    return SuccessResponse()


@router.post("/tournaments/{tournament_id}/rounds", tags = ["Rounds"], response_model=SuccessResponse)
async def create_round(
    tournament_id: TournamentId,
    round_body: RoundCreateBody,
    user: User_propelauth = Depends(auth.require_user),
) -> SuccessResponse:
    public_user = await get_user_by_id(assert_some(user.properties['bracket_id']))
    await check_foreign_keys_belong_to_tournament(round_body, tournament_id)

    stages = await get_full_tournament_details(tournament_id)
    existing_rounds = [
        round_
        for stage in stages
        for stage_item in stage.stage_items
        for round_ in stage_item.rounds
    ]
    check_requirement(existing_rounds, public_user, "max_rounds")

    stage_item = await get_stage_item(tournament_id, stage_item_id=round_body.stage_item_id)

    if stage_item is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Stage item doesn't exist",
        )

    if not stage_item.type.supports_dynamic_number_of_rounds:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Stage type {stage_item.type} doesn't support manual creation of rounds",
        )

    round_id = await sql_create_round(
        RoundToInsert(
            stage_item_id=round_body.stage_item_id,
            name=await get_next_round_name(tournament_id, round_body.stage_item_id),
        ),
    )

    await set_round_active_or_draft(round_id, tournament_id, is_active=False, is_draft=True)
    return SuccessResponse()


@router.put("/tournaments/{tournament_id}/rounds/{round_id}", tags = ["Rounds"], response_model=SuccessResponse)
async def update_round_by_id(
    tournament_id: TournamentId,
    round_id: RoundId,
    round_body: RoundUpdateBody,
    _: User_propelauth = Depends(auth.require_user),
    __: Round = Depends(round_dependency),
) -> SuccessResponse:
    await set_round_active_or_draft(
        round_id, tournament_id, is_active=round_body.is_active, is_draft=round_body.is_draft
    )
    query = """
        UPDATE rounds
        SET name = :name
        WHERE rounds.id IN (
            SELECT rounds.id
            FROM rounds
            JOIN stage_items ON rounds.stage_item_id = stage_items.id
            JOIN stages s on s.id = stage_items.stage_id
            WHERE s.tournament_id = :tournament_id
        )
        AND rounds.id = :round_id
    """
    await database.execute(
        query=query,
        values={"tournament_id": tournament_id, "round_id": round_id, "name": round_body.name},
    )
    return SuccessResponse()
