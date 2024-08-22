from pydantic import BaseModel

class VoterBase(BaseModel):
    address: str

class VoterCreate(VoterBase):
    pass

class Voter(VoterBase):
    id: int
    has_voted: bool

    class Config:
        orm_mode = True

class VoteBase(BaseModel):
    candidate_id: int

class VoteCreate(VoteBase):
    voter_id: int

class Vote(VoteBase):
    id: int
    voter_id: int

    class Config:
        orm_mode = True
