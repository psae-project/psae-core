from datetime import datetime, timezone
from psae.types.events import PresidentialEvent, SentimentSignal, PolicyDomain, EntityMention


def test_presidential_event_hash():
    event = PresidentialEvent(
        id="test_001",
        timestamp=datetime(2020, 1, 1, tzinfo=timezone.utc),
        source="tweet",
        speaker="POTUS",
        raw_text="We are imposing 25% tariffs on Chinese steel.",
    )
    assert len(event.content_hash) == 64
    assert event.content_hash != ""


def test_sentiment_signal_creation():
    sig = SentimentSignal(
        event_id="test_001",
        timestamp=datetime(2020, 1, 1, tzinfo=timezone.utc),
        overall_sentiment=-0.72,
        confidence=0.85,
        policy_domains=[PolicyDomain(domain="trade", confidence=0.9, direction=-0.72)],
        entity_mentions=[EntityMention(text="China", label="GPE", ticker="FXI", sector="International")]
    )
    assert sig.overall_sentiment == -0.72
    assert len(sig.policy_domains) == 1
    assert sig.policy_domains[0].domain == "trade"
