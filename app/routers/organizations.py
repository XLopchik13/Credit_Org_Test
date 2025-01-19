from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from geopy.distance import geodesic
from sqlalchemy.orm import selectinload

from app.database import get_db
from app.models import Organization, organization_activity, Building, Activity
from app.schemas import OrganizationResponse

router = APIRouter(
    prefix="/organizations",
    tags=["Organizations"]
)


@router.get("/", response_model=List[OrganizationResponse])
async def get_all_organizations(
        db: AsyncSession = Depends(get_db)
):
    query = await db.execute(
        select(Organization).options(selectinload(Organization.activities))
    )
    activities = query.scalars().all()
    return [OrganizationResponse.from_orm(activity) for activity in activities]


@router.get("/by-building/{building_id}", response_model=List[OrganizationResponse])
async def get_organizations_by_building(
    building_id: int, db: AsyncSession = Depends(get_db)
):
    query = await db.execute(
        select(Organization)
        .where(Organization.building_id == building_id)
        .options(selectinload(Organization.activities))
    )
    organizations = query.scalars().all()
    return organizations


@router.get("/by-activity/{activity_id}", response_model=List[OrganizationResponse])
async def get_organizations_by_activity(
    activity_id: int, db: AsyncSession = Depends(get_db)
):
    query = await db.execute(
        select(Organization)
        .join(organization_activity)
        .where(organization_activity.c.activity_id == activity_id)
        .options(selectinload(Organization.activities))
    )
    organizations = query.scalars().all()
    return organizations


@router.get("/nearby", response_model=List[OrganizationResponse])
async def get_organizations_nearby(
    latitude: float,
    longitude: float,
    radius: float,
    db: AsyncSession = Depends(get_db),
):
    query = await db.execute(select(Building))
    buildings = query.scalars().all()

    nearby_buildings = [
        building
        for building in buildings
        if geodesic((latitude, longitude), (building.latitude, building.longitude)).km <= radius
    ]

    building_ids = [building.id for building in nearby_buildings]

    query = await db.execute(
        select(Organization)
        .where(Organization.building_id.in_(building_ids))
        .options(selectinload(Organization.activities))
    )
    organizations = query.scalars().all()
    return organizations


@router.get("/{organization_id}", response_model=OrganizationResponse)
async def get_organization_by_id(
    organization_id: int, db: AsyncSession = Depends(get_db)
):
    query = await db.execute(
        select(Organization)
        .where(Organization.id == organization_id)
        .options(selectinload(Organization.activities))
    )
    organization = query.scalar_one_or_none()
    if not organization:
        raise HTTPException(status_code=404, detail="Organization not found")
    return organization


@router.get("/by-activity-tree/{activity_id}", response_model=List[OrganizationResponse])
async def get_organizations_by_activity_tree(
    activity_id: int, db: AsyncSession = Depends(get_db)
):
    def get_all_children(activity, visited):
        visited.add(activity.id)
        for child in activity.children:
            if child.id not in visited:
                get_all_children(child, visited)
        return visited

    query = await db.execute(
        select(Activity)
        .where(Activity.id == activity_id)
    )
    root_activity = query.scalar_one_or_none()
    if not root_activity:
        raise HTTPException(status_code=404, detail="Activity not found")

    activity_ids = get_all_children(root_activity, set())

    query = await db.execute(
        select(Organization)
        .join(organization_activity)
        .where(organization_activity.c.activity_id.in_(activity_ids))
        .options(selectinload(Organization.activities))
    )
    organizations = query.scalars().all()
    return organizations


@router.get("/search/{name}", response_model=List[OrganizationResponse])
async def search_organizations_by_name(
    name: str, db: AsyncSession = Depends(get_db)
):
    query = await db.execute(
        select(Organization)
        .where(Organization.name == name)
        .options(selectinload(Organization.activities))

    )
    organizations = query.scalars().all()
    return organizations
