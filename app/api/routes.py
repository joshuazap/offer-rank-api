from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import Consumer, Offer
from app.schemas import ConsumerOut, HealthOut, OfferOut, RankResponse
from app.services.ranking import rank_offers_for_consumer

router = APIRouter()


@router.get("/health", response_model=HealthOut)
def health() -> HealthOut:
    return HealthOut(status="ok")


@router.get("/consumers", response_model=list[ConsumerOut])
def list_consumers(db: Session = Depends(get_db)) -> list[Consumer]:
    return list(db.scalars(select(Consumer).order_by(Consumer.id)).all())


@router.get("/offers", response_model=list[OfferOut])
def list_offers(db: Session = Depends(get_db)) -> list[Offer]:
    return list(db.scalars(select(Offer).where(Offer.active.is_(True)).order_by(Offer.id)).all())


@router.get("/consumers/{external_id}/recommendations", response_model=RankResponse)
def recommendations(
    external_id: str,
    limit: int = Query(default=5, ge=1, le=50),
    db: Session = Depends(get_db),
) -> RankResponse:
    try:
        return rank_offers_for_consumer(db, external_id=external_id, limit=limit)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
