from sqlalchemy import Column, Integer, String, ForeignKey, Float, Table
from sqlalchemy.orm import relationship

from app.database import Base

organization_activity = Table(
    'organization_activity', Base.metadata,
    Column('organization_id', Integer, ForeignKey('organizations.id'), primary_key=True),
    Column('activity_id', Integer, ForeignKey('activities.id'), primary_key=True)
)


class Building(Base):
    __tablename__ = 'buildings'

    id = Column(Integer, primary_key=True, index=True)
    address = Column(String, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)

    organizations = relationship("Organization", back_populates="buildings")


class Activity(Base):
    __tablename__ = 'activities'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    parent_id = Column(Integer, ForeignKey('activities.id'), nullable=True)

    parent = relationship("Activity", remote_side=[id], backref="children")
    children = relationship("Activity", back_populates="parent")
    organizations = relationship("Organization", secondary=organization_activity, back_populates="activities")


class Organization(Base):
    __tablename__ = 'organizations'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    phone_numbers = Column(String, nullable=True)
    building_id = Column(Integer, ForeignKey('buildings.id'))

    building = relationship("Building", back_populates="organizations")
    activities = relationship("Activity", secondary=organization_activity, backref="organizations")
