from datetime import datetime, timedelta, timezone

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.db import SessionLocal
from app.models import Consumer, Event, Offer


def seed_if_empty() -> None:
    db: Session = SessionLocal()
    try:
        consumer_count = db.scalar(select(func.count()).select_from(Consumer)) or 0
        if consumer_count > 0:
            return

        consumers = [
            Consumer(external_id="c_alex", segment="value_seeker"),
            Consumer(external_id="c_blake", segment="premium"),
            Consumer(external_id="c_casey", segment="new"),
        ]
        offers = [
            Offer(sku="SKU-TEA-01", title="Organic Green Tea 20ct", category="grocery", margin_score=0.42),
            Offer(sku="SKU-SOAP-02", title="Botanical Bar Soap", category="personal_care", margin_score=0.61),
            Offer(sku="SKU-BAG-03", title="Reusable Tote", category="home", margin_score=0.35),
            Offer(sku="SKU-SERUM-04", title="Vitamin C Serum", category="personal_care", margin_score=0.78),
            Offer(sku="SKU-SNACK-05", title="Protein Trail Mix", category="grocery", margin_score=0.55),
        ]
        db.add_all(consumers + offers)
        db.flush()

        now = datetime.now(timezone.utc)
        alex, blake, casey = consumers
        tea, soap, tote, serum, snack = offers

        events = [
            Event(consumer_id=alex.id, offer_id=tea.id, event_type="view", category="grocery", occurred_at=now - timedelta(days=1)),
            Event(consumer_id=alex.id, offer_id=snack.id, event_type="click", category="grocery", occurred_at=now - timedelta(hours=6)),
            Event(consumer_id=alex.id, offer_id=soap.id, event_type="view", category="personal_care", occurred_at=now - timedelta(days=10)),
            Event(consumer_id=blake.id, offer_id=serum.id, event_type="purchase", category="personal_care", occurred_at=now - timedelta(days=2)),
            Event(consumer_id=blake.id, offer_id=soap.id, event_type="click", category="personal_care", occurred_at=now - timedelta(days=1)),
            Event(consumer_id=blake.id, offer_id=tote.id, event_type="view", category="home", occurred_at=now - timedelta(days=20)),
            Event(consumer_id=casey.id, offer_id=tote.id, event_type="view", category="home", occurred_at=now - timedelta(hours=3)),
        ]
        db.add_all(events)
        db.commit()
    finally:
        db.close()
