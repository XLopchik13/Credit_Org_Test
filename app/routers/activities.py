from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import Activity
from app.schemas import ActivityResponse

router = APIRouter(
    prefix="/by_activity",
    tags=["Activities"]
)


@router.get("/", response_model=List[ActivityResponse])
async def get_all_activities(db: AsyncSession = Depends(get_db)):
    query = await db.execute(select(Activity))
    activities = query.scalars().all()
    return [ActivityResponse.from_orm(activity) for activity in activities]
