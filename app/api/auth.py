from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from common import auth
from app.schemas import signUp, TokenResponse, LoginData
from app.database import get_async_db
from app.models import User

import re

router = APIRouter(prefix="/auth", tags=["AUTH"])


@router.post("/sign-up", response_model=TokenResponse)
async def sign_up(  # type:ignore
    data: signUp, db: AsyncSession = Depends(get_async_db)
):
    login_query = await db.execute(select(User).where(User.login == data.login))
    login_exist = login_query.scalars().first()

    if login_exist:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=f"{data.login} already exist"
        )

    phone_query = await db.execute(select(User).where(User.phone == data.phone))
    phone_exist = phone_query.scalars().first()

    if phone_exist:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=f"{data.phone} already exist"
        )
    fio_regex = r"^[A-Z][a-z]+(?:\s[A-Z][a-z]+){1,2}$"

    if not re.match(fio_regex, data.fio):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="fio must be at least 2 characters and capitalized",
        )

    if not len(data.phone) != 9:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="phone must be 9 characters"
        )
    login_regex = r"^[a-z0-9]+$"

    if not re.match(login_regex, data.login) or len(data.login) < 6:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="login must be str and number",
        )

    new_user = User(
        fio=data.fio,
        login=data.login,
        phone=data.phone,
        password=auth.hash_password(data.password),
        birthday=data.birthday,
        gender=data.gender,
        address=data.address,
        role=data.role,
    )
    db.add(new_user)
    await db.commit()

    tokens = auth.create_tokens(data.login)

    return {
        "accessToken": tokens.get("accessToken"),
        "refreshToken": tokens.get("refreshToken"),
        "role": data.role,
    }  # type:ignore


@router.post("/login", response_model=TokenResponse)
async def login_end(
    data: LoginData, db: AsyncSession = Depends(get_async_db)
):  # type:ignore
    login_query = await db.execute(select(User).where(User.login == data.login))
    db_user = login_query.scalars().first()

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid credentials"
        )

    if not auth.verify_password(
        plain_password=data.password, hashed_password=db_user.password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid credentials"
        )

    tokens = auth.create_tokens(data.login)

    return {
        "accessToken": tokens.get("accessToken"),
        "refreshToken": tokens.get("refreshToken"),
        "role": db_user.role,
    }  # type:ignore
