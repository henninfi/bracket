from fastapi import APIRouter, Depends
from fastapi.responses import PlainTextResponse

from bracket.models.metrics import get_request_metrics
from bracket.utils.limits_wrapper import RateLimitMiddleware
from bracket.utils.limits_wrapper import rate_provider

router = APIRouter()



@router.get("/metrics", tags=["Internals"], response_class=PlainTextResponse, )
async def get_metrics() -> PlainTextResponse:
    return PlainTextResponse(get_request_metrics().to_prometheus())


@router.get("/ping", tags=["Internals"], summary="Healthcheck ping")
async def ping() -> str:
    return "ping"
