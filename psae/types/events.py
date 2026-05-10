from __future__ import annotations
from datetime import datetime
from typing import Literal
from pydantic import BaseModel, Field
import hashlib

SourceType = Literal[
    "truth_social", "speech", "press_briefing",
    "executive_order", "tweet", "press_release"
]


class PresidentialEvent(BaseModel):
    id: str
    timestamp: datetime
    source: SourceType
    speaker: str  # "POTUS", "SecTreasury", "FedChair"
    raw_text: str
    url: str | None = None
    content_hash: str = ""
    metadata: dict = Field(default_factory=dict)

    def model_post_init(self, __context):
        if not self.content_hash:
            self.content_hash = hashlib.sha256(self.raw_text.encode()).hexdigest()


class EntityMention(BaseModel):
    text: str
    label: str  # "ORG", "GPE", "PERSON"
    ticker: str | None = None
    sector: str | None = None
    confidence: float = 0.85


class PolicyDomain(BaseModel):
    domain: str
    confidence: float
    direction: float  # [-1, 1]


class SentimentSignal(BaseModel):
    event_id: str
    timestamp: datetime
    overall_sentiment: float  # [-1, 1]
    policy_domains: list[PolicyDomain] = Field(default_factory=list)
    entity_mentions: list[EntityMention] = Field(default_factory=list)
    confidence: float
    model_version: str = "psae-signal-v0.1.0"
    holding_period_hint: str = "4h"


class AssetSignal(BaseModel):
    ticker: str
    direction: float  # [-1, 1]
    conviction: float  # [0, 1]
    reason: str = ""


class TradeSignal(BaseModel):
    signal_id: str
    source_signal_id: str
    generated_at: datetime
    asset_signals: list[AssetSignal] = Field(default_factory=list)
    beta_neutrality_score: float = 0.0
    expected_holding_period: str = "4h"
    regime: str = "neutral"
    gross_exposure: float = 1.0
