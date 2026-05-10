import json
import redis
from typing import Callable, Any
from psae.config.settings import settings


class StreamConsumer:
    def __init__(self, stream: str, group: str, consumer_name: str):
        self.r = redis.from_url(settings.redis_url, decode_responses=True)
        self.stream = stream
        self.group = group
        self.consumer_name = consumer_name
        self._ensure_group()

    def _ensure_group(self):
        try:
            self.r.xgroup_create(self.stream, self.group, id="0", mkstream=True)
        except redis.exceptions.ResponseError:
            pass  # Group already exists

    def consume(self, handler: Callable[[dict], Any], block_ms: int = 5000):
        """Blocking consumer loop. Calls handler(data_dict) for each message."""
        while True:
            messages = self.r.xreadgroup(
                self.group, self.consumer_name,
                {self.stream: ">"}, count=10, block=block_ms
            )
            if not messages:
                continue
            for _, msg_list in messages:
                for msg_id, fields in msg_list:
                    data = json.loads(fields["data"])
                    handler(data)
                    self.r.xack(self.stream, self.group, msg_id)
