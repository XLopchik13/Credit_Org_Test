from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import Building
from app.schemas import BuildingResponse

router = APIRouter(
    prefix="/by_building",
    tags=["Buildings"]
)


@router.get("/", response_model=List[BuildingResponse])
async def get_all_buildings(db: AsyncSession = Depends(get_db)):
    query = await db.execute(select(Building))
    buildings = query.scalars().all()
    return buildings

