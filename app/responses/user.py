from typing import Tuple
import aiohttp

from ..config import API_URL


async def get_current_user(token: str) -> Tuple[int, dict]:
    async with aiohttp.ClientSession(API_URL) as session:
        async with session.get(
            "/user/me", headers={"Authorization": f"Bearer {token}"}
        ) as response:
            return response.status, await response.json()