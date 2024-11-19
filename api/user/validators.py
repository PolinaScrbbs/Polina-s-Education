from .models import User
from .schemes import BaseUser


async def user_to_pydantic(user: User) -> BaseUser:
    return BaseUser(
        id=user.id, username=user.username, role=user.role, full_name=user.full_name
    )
