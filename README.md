# psae-core

Shared foundation for the **Presidential Sentiment Alpha Engine** — types, config, message bus, and utilities used by all PSAE repos.

## Installation

```bash
pip install psae-core
```

## What's inside

| Module | Purpose |
|--------|---------|
| `psae.types.events` | Core data contracts: `PresidentialEvent`, `SentimentSignal`, `TradeSignal` |
| `psae.config.settings` | Pydantic-based config (env-var driven) |
| `psae.bus.producer` | Redis Streams producer |
| `psae.bus.consumer` | Redis Streams consumer (consumer group) |
| `psae.utils.time` | NYSE market calendar utilities |

## Quick example

```python
from psae.types.events import PresidentialEvent, SentimentSignal
from psae.bus.producer import StreamProducer
from datetime import datetime, timezone

event = PresidentialEvent(
    id="tw_123456",
    timestamp=datetime.now(timezone.utc),
    source="tweet",
    speaker="POTUS",
    raw_text="We are imposing a 25% tariff on all Chinese steel imports."
)

producer = StreamProducer()
producer.publish_event(event)
```

## Part of the PSAE ecosystem

```
psae-core  ← you are here
psae-ingest  → ingests presidential communications
psae-signal  → extracts NLP sentiment signals
psae-factor  → factor analysis & IC tear sheets (≈ Alphalens)
psae-backtest → event-driven backtesting (≈ Zipline)
psae-folio   → portfolio analytics (≈ Pyfolio)
```

## License
Apache 2.0
