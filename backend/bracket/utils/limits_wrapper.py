from limits import RateLimitItem, RateLimitItemPerMinute, storage, strategies
from starlette.requests import Request
from starlette.exceptions import HTTPException
from starlette.status import HTTP_429_TOO_MANY_REQUESTS
import redis

import redis

r = redis.Redis(
  host='redis-16890.c327.europe-west1-2.gce.redns.redis-cloud.com',
  port=16890,
  password='wz4EZsr0xnHtmc801v0J0rygmLpGANek')


REDIS_URL: str = "redis://default:wz4EZsr0xnHtmc801v0J0rygmLpGANek@redis-16890.c327.europe-west1-2.gce.redns.redis-cloud.com:16890"
storage = storage.RedisStorage(REDIS_URL)
throttler = strategies.MovingWindowRateLimiter(storage)

"""
    This component is used as a wrapper for `limits` so we won't use its api directly in the throttler class.
"""


def hit(key: str, rate_per_minute: int, cost: int = 1) -> bool:
    """
        Hits the throttler and returns `true` if a request can be passed and `false` if it needs to be blocked
        :param key: the key that identifies the client that needs to be throttled
        :param rate_per_minute: the number of request per minute to allow
        :param cost: the cost of the request in the time window.
        :return: returns `true` if a request can be passed and `false` if it needs to be blocked
    """
    item = rate_limit_item_for(rate_per_minute=rate_per_minute)
    is_hit = throttler.hit(item, key, cost=cost)
    return is_hit


def rate_limit_item_for(rate_per_minute: int) -> RateLimitItem:
    """
    Returns the rate of requests for a specific model

    :param rate_per_minute: the number of request per minute to allow
    :return: `RateLimitItem` object initiated with a rate limit that matched the model
    """
    return RateLimitItemPerMinute(rate_per_minute)


from typing import Callable, Awaitable, Any

async def identifier(request: Request) -> str:
  ip = request.client.host
  return ip

async def _default_callback(request: Request):
    raise HTTPException(status_code=HTTP_429_TOO_MANY_REQUESTS, detail="request limit reached")

class RateLimitMiddleware:
    def __init__(
        self,
        rate_provider: Callable[[Request], Awaitable[int]],
        callback: Callable[[Request], Awaitable[Any]] = _default_callback,
        identifier: Callable[[Request], Awaitable[str]] = identifier
    ):
        self.identifier = identifier
        self.callback = callback
        self.rate_provider = rate_provider

    async def __call__(self, request: Request):
        callback = self.callback
        identifier = self.identifier
        rate_provider = self.rate_provider

        key = await identifier(request)
        rate = await rate_provider(request)

        if not hit(key=key, rate_per_minute=rate):
            return await callback(request)
        
async def rate_provider(request: Request) -> str:
  return 300
