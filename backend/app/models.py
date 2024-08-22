from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base

class Voter(Base):
    __tablename__ = "voters"

    id = Column(Integer, primary_key=True, index=True)
    address = Column(String, unique=True, index=True)
    has_voted = Column(Boolean, default=False)

    votes = relationship("Vote", back_populates="voter")

class Vote(Base):
    __tablename__ = "votes"

    id = Column(Integer, primary_key=True, index=True)
    voter_id = Column(Integer, ForeignKey("voters.id"))
    candidate_id = Column(Integer)

    voter = relationship("Voter", back_populates="votes")
