from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import with_polymorphic, selectin_polymorphic
from fastapi import HTTPException
from sqlalchemy import select
from core.db_helper import db_helper
from core.models import User, Teacher, Student
from core.schemas import UserCreateInDB
from core.constants import error_when_adding_user_to_db
from core.db_helper import postgres_session


async def get_user_by_id(
    user_id: int,
) -> Teacher | Student | None:
    session: AsyncSession = postgres_session.get()
    # Fetch user with polymorphic loading to include role-specific fields
    user_polymorphic = with_polymorphic(User, [Teacher, Student])
    stmt = select(user_polymorphic).where(user_polymorphic.id == user_id)
    user = await session.scalar(stmt)
    return user


async def get_user_by_username(
    username: str,
) -> Teacher | Student | None:
    session: AsyncSession = postgres_session.get()
    # Fetch user with polymorphic loading to include role-specific fields
    user_polymorphic = with_polymorphic(User, [Teacher, Student])
    stmt = select(user_polymorphic).where(user_polymorphic.username == username)
    user = await session.scalar(stmt)
    print(user)
    return user


async def add_user_to_db(
    user: UserCreateInDB,
):
    session: AsyncSession = postgres_session.get()
    try:
        print(user.model_dump())
        if user.role_type == "teacher":
            user = Teacher(**user.model_dump(), subject=None)
        if user.role_type == "student":
            user = Student(**user.model_dump())
        session.add(user)
        await session.commit()
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e),
        )
    return user
