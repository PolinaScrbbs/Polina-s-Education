import aiohttp

from ..config import API_URL


async def registraion(
    username: str,
    password: str,
    confirm_password: str,
    full_name: str,
):
    async with aiohttp.ClientSession(API_URL) as session:
        async with session.post(
            "/auth/registration",
            json={
                "username": username,
                "password": password,
                "confirm_password": confirm_password,
                "full_name": full_name,
            },
        ) as response:
            return response.status
