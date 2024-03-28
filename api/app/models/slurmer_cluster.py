import random
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database.engine import Base


class SlurmerCluster(Base):
    __tablename__ = "slurmer-clusters"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

    url = Column(String)
    token = Column(String)
    user = Column(String)

    start_port = Column(Integer)
    end_port = Column(Integer)

    created = Column(DateTime(timezone=True), server_default=func.now())
    updated = Column(DateTime(timezone=True), onupdate=func.now())

    def random_port(self):
        return random.randint(self.start_port, self.end_port)
