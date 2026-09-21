from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base


class Consumer(Base):
    __tablename__ = "consumers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    external_id: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    segment: Mapped[str] = mapped_column(String(64), index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    events: Mapped[list["Event"]] = relationship(back_populates="consumer")


class Offer(Base):
    __tablename__ = "offers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    sku: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    title: Mapped[str] = mapped_column(String(200))
    category: Mapped[str] = mapped_column(String(64), index=True)
    margin_score: Mapped[float] = mapped_column(Float, default=0.5)
    active: Mapped[bool] = mapped_column(default=True)


class Event(Base):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    consumer_id: Mapped[int] = mapped_column(ForeignKey("consumers.id"), index=True)
    offer_id: Mapped[int | None] = mapped_column(ForeignKey("offers.id"), nullable=True)
    event_type: Mapped[str] = mapped_column(String(32), index=True)  # view | click | purchase
    category: Mapped[str] = mapped_column(String(64), index=True)
    occurred_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    consumer: Mapped["Consumer"] = relationship(back_populates="events")
