from sqlalchemy.orm import Session
from sqlalchemy import func
from . import models, schemas
from fastapi import HTTPException
from typing import Any

def get_voter(db: Session, voter_id: int) -> Any:
    return db.query(models.Voter).filter(models.Voter.id == voter_id).first()

def get_voter_by_address(db: Session, address: str) -> Any:
    return db.query(models.Voter).filter(models.Voter.address == address).first()

def create_voter(db: Session, voter: schemas.VoterCreate) -> models.Voter:
    db_voter = models.Voter(address=voter.address)
    db.add(db_voter)
    db.commit()
    db.refresh(db_voter)
    return db_voter

def create_vote(db: Session, vote: schemas.VoteCreate) -> models.Vote:
    db_voter = get_voter(db, vote.voter_id)
    if db_voter is None:
        raise HTTPException(status_code=404, detail="Voter not found")

    # Type ignore for Pyright
    if db_voter.has_voted:  # type: ignore
        raise HTTPException(status_code=400, detail="Voter has already cast a vote")

    db_vote = models.Vote(voter_id=vote.voter_id, candidate_id=vote.candidate_id)
    # Type ignore for Pyright
    db_voter.has_voted = True  # type: ignore
    db.add(db_vote)
    db.commit()
    db.refresh(db_vote)
    return db_vote

def get_vote_results(db: Session) -> list[dict[str, Any]]:
    votes = db.query(models.Vote.candidate_id, func.count(models.Vote.id).label('vote_count')) \
        .group_by(models.Vote.candidate_id) \
        .all()
    return [{"candidate_id": vote.candidate_id, "vote_count": vote.vote_count} for vote in votes]
