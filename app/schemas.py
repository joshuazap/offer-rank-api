from datetime import datetime

from pydantic import BaseModel, Field


class HealthOut(BaseModel):
    status: str


class ConsumerOut(BaseModel):
    id: int
    external_id: str
    segment: str

    model_config = {"from_attributes": True}


class OfferOut(BaseModel):
    id: int
    sku: str
    title: str
    category: str
    margin_score: float

    model_config = {"from_attributes": True}


class RankedOfferOut(BaseModel):
    offer: OfferOut
    score: float = Field(..., description="Explainable composite score 0..1")
    reasons: list[str]


class RankResponse(BaseModel):
    consumer_id: str
    ranked: list[RankedOfferOut]
    generated_at: datetime
