from fastapi import FastAPI

from app.routers.organizations import router as organization_router
from app.routers.activities import router as activities_router
from app.routers.buildings import router as buildings_router

app = FastAPI()

app.include_router(organization_router)
app.include_router(activities_router)
app.include_router(buildings_router)
