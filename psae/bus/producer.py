import json
import redis
from psae.config.settings import settings
from psae.types.events import PresidentialEvent, SentimentSignal, TradeSignal


class StreamProducer:
    def __init__(self):
        self.r = redis.from_url(settings.redis_url, decode_responses=True)

    def publish_event(self, event: PresidentialEvent) -> str:
        msg_id = self.r.xadd(
            settings.event_stream,
            {"data": event.model_dump_json()},
            maxlen=10_000,
        )
        return msg_id

    def publish_signal(self, signal: SentimentSignal) -> str:
        msg_id = self.r.xadd(
            settings.signal_stream,
            {"data": signal.model_dump_json()},
            maxlen=10_000,
        )
        return msg_id

    def publish_trade(self, trade: TradeSignal) -> str:
        msg_id = self.r.xadd(
            settings.trade_stream,
            {"data": trade.model_dump_json()},
            maxlen=5_000,
        )
        return msg_id
