from fastapi import APIRouter, Depends, Body
from sqlalchemy import select
from auth.router import user_dependency
from database import db_dependency
from models.schemas import *
from models.orm import *

contest_router = APIRouter(prefix='/contest')

@contest_router.post('/add/')
async def add_contest(
        user: user_dependency,
        db: db_dependency,
        contest_name: str = Body(...)
) -> ContestBase:
    contest: Contest = Contest(
        name=contest_name,
        owner_id=user.id
    )

    db.add(contest)
    await db.commit()

    return ContestBase.from_orm(contest)

@contest_router.get('/created/')
async def get_created_contests(
        user: user_dependency,
        db: db_dependency
) -> List[ContestBase]:
    user: User = await db.get(User, user.id)
    return [ContestBase.from_orm(contest) for contest in user.created_contests]


@contest_router.get('/participated/')
async def get_participated_contests(
        user: user_dependency,
        db: db_dependency
) -> List[ContestBase]:
    user: User = await db.get(User, user.id)
    return [ContestBase.from_orm(contest) for contest in user.participated_contests]


@contest_router.get('/available/')
async def get_available_contests(
        user: user_dependency,
        db: db_dependency
) -> List[ContestBase]:
    stmt = select(Contest).filter((Contest.owner_id != user.id) &
                                  ~(Contest.participants.any(User.id == user.id)))
    contests: List[Contest] = (await db.execute(stmt)).scalars().all()
    return [ContestBase.from_orm(contest) for contest in contests]

@contest_router.post('/join_contest/')
async def join_contest(
        user: user_dependency,
        db: db_dependency,
        contest_id: int = Body(...)
) -> None:
    user_contest: UserContest = UserContest(
        contest_id=contest_id,
        participant_id=user.id
    )

    db.add(user_contest)
    await db.commit()