from pydantic import BaseModel

class RankingResponse(BaseModel):
    llm: str
    mean_value: float
    rank: int

    class Config:
        orm_mode = True
