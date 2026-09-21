from collections import defaultdict
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.config import settings
from app.models import Consumer, Event, Offer
from app.schemas import OfferOut, RankedOfferOut, RankResponse


EVENT_WEIGHT = {"view": 1.0, "click": 3.0, "purchase": 8.0}


def rank_offers_for_consumer(db: Session, external_id: str, limit: int = 10) -> RankResponse:
    consumer = db.scalar(select(Consumer).where(Consumer.external_id == external_id))
    if consumer is None:
        raise ValueError(f"Unknown consumer: {external_id}")

    offers = list(db.scalars(select(Offer).where(Offer.active.is_(True))).all())
    events = list(db.scalars(select(Event).where(Event.consumer_id == consumer.id)).all())

    affinity_by_category: dict[str, float] = defaultdict(float)
    last_touch: dict[str, datetime] = {}
    now = datetime.now(timezone.utc)

    for event in events:
        affinity_by_category[event.category] += EVENT_WEIGHT.get(event.event_type, 1.0)
        occurred = event.occurred_at
        if occurred.tzinfo is None:
            occurred = occurred.replace(tzinfo=timezone.utc)
        prev = last_touch.get(event.category)
        if prev is None or occurred > prev:
            last_touch[event.category] = occurred

    max_affinity = max(affinity_by_category.values(), default=1.0) or 1.0

    ranked: list[RankedOfferOut] = []
    for offer in offers:
        raw_affinity = affinity_by_category.get(offer.category, 0.0)
        affinity = raw_affinity / max_affinity

        touched = last_touch.get(offer.category)
        if touched is None:
            recency = 0.1
        else:
            age_hours = max((now - touched).total_seconds() / 3600.0, 0.0)
            recency = max(0.0, 1.0 - min(age_hours / (24 * 14), 1.0))  # fades over 14 days

        margin = max(0.0, min(offer.margin_score, 1.0))
        score = (
            settings.weight_affinity * affinity
            + settings.weight_recency * recency
            + settings.weight_margin * margin
        )

        reasons = [
            f"affinity={affinity:.2f} for category '{offer.category}'",
            f"recency={recency:.2f}",
            f"margin={margin:.2f}",
        ]
        ranked.append(
            RankedOfferOut(
                offer=OfferOut.model_validate(offer),
                score=round(score, 4),
                reasons=reasons,
            )
        )

    ranked.sort(key=lambda row: row.score, reverse=True)
    return RankResponse(
        consumer_id=external_id,
        ranked=ranked[:limit],
        generated_at=now,
    )
