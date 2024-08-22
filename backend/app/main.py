from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/voters/", response_model=schemas.Voter)
def create_voter(voter: schemas.VoterCreate, db: Session = Depends(get_db)):
    db_voter = crud.get_voter_by_address(db, address=voter.address)
    if db_voter:
        raise HTTPException(status_code=400, detail="Address already registered")
    return crud.create_voter(db=db, voter=voter)

@app.get("/voters/{voter_id}", response_model=schemas.Voter)
def read_voter(voter_id: int, db: Session = Depends(get_db)):
    db_voter = crud.get_voter(db, voter_id=voter_id)
    if db_voter is None:
        raise HTTPException(status_code=404, detail="Voter not found")
    return db_voter

@app.post("/vote/", response_model=schemas.Vote)
def create_vote(vote: schemas.VoteCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_vote(db=db, vote=vote)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/results/")
def read_results(db: Session = Depends(get_db)):
    return crud.get_vote_results(db)
