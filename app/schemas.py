from pydantic import BaseModel, Field
from typing import List, Optional


class BuildingBase(BaseModel):
    pass


class BuildingCreate(BuildingBase):
    pass


class BuildingResponse(BuildingBase):
    id: int
    address: str
    latitude: float
    longitude: float

    class Config:
        from_attributes = True


class ActivityBase(BaseModel):
    pass


class ActivityCreate(ActivityBase):
    parent_id: Optional[int] = None


class ActivityResponse(ActivityBase):
    id: int
    name: str
    parent_id: Optional[int] = None

    class Config:
        from_attributes = True


ActivityResponse.update_forward_refs()


class OrganizationBase(BaseModel):
    pass


class OrganizationCreate(OrganizationBase):
    activity_ids: List[int] = Field(
        ..., example=[1, 2]
    )


class OrganizationResponse(OrganizationBase):
    id: int
    name: str
    phone_numbers: List[str]
    building_id: int
    activities: List[ActivityResponse]

    class Config:
        from_attributes = True
