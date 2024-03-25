from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database.engine import Base


class Instance(Base):
    __tablename__ = "instances"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    assign_to = Column(String, index=True)

    tunnel_instance_id = Column(String, index=True)
    port = Column(Integer)
    map_to_port = Column(Integer)

    package_id = Column(Integer)
    image_id = Column(Integer)
    slurmer_id = Column(Integer)

    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="instances")

    created = Column(DateTime(timezone=True), server_default=func.now())
    updated = Column(DateTime(timezone=True), onupdate=func.now())
