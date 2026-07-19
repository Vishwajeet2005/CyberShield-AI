"""
CyberShield AI — Kafka Streaming Pipeline
==========================================
Replaces the asyncio in-memory simulator loop with a real Kafka event stream.

Topics:
  telemetry.raw      — raw entity feature vectors (producer: simulator + ingest API)
  anomalies.scored   — events that exceeded anomaly threshold (producer: BADE consumer)
  incidents.created  — new incident signals for AIRO (producer: AAPA)

Falls back gracefully if Kafka broker is unavailable.
"""

import asyncio
import json
import logging
from datetime import datetime, timezone
from typing import Callable, Optional, AsyncGenerator

logger = logging.getLogger("cybershield.kafka")

KAFKA_BOOTSTRAP = "localhost:9092"

TOPIC_TELEMETRY  = "telemetry.raw"
TOPIC_ANOMALIES  = "anomalies.scored"
TOPIC_INCIDENTS  = "incidents.created"

ALL_TOPICS = [TOPIC_TELEMETRY, TOPIC_ANOMALIES, TOPIC_INCIDENTS]

# ─── Availability check ────────────────────────────────────────────────────────

_kafka_available: Optional[bool] = None

async def check_kafka() -> bool:
    global _kafka_available
    if _kafka_available is not None:
        return _kafka_available
    try:
        from aiokafka import AIOKafkaProducer
        prod = AIOKafkaProducer(bootstrap_servers=KAFKA_BOOTSTRAP)
        await asyncio.wait_for(prod.start(), timeout=3.0)
        await prod.stop()
        _kafka_available = True
        logger.info("Kafka broker reachable at %s", KAFKA_BOOTSTRAP)
    except Exception as e:
        _kafka_available = False
        logger.warning("Kafka unavailable (%s). Event streaming will use in-memory fallback.", e)
    return _kafka_available


# ─── Producer ─────────────────────────────────────────────────────────────────

class KafkaProducer:
    """
    Async Kafka producer with automatic JSON serialization.
    Silently no-ops if Kafka is unavailable.
    """
    def __init__(self):
        self._producer = None
        self._available = False

    async def start(self):
        if not await check_kafka():
            return
        try:
            from aiokafka import AIOKafkaProducer
            self._producer = AIOKafkaProducer(
                bootstrap_servers=KAFKA_BOOTSTRAP,
                value_serializer=lambda v: json.dumps(v).encode("utf-8"),
                key_serializer=lambda k: k.encode("utf-8") if k else None,
                compression_type="gzip",
                acks="all",                  # Wait for all replicas
                enable_idempotence=True,     # Exactly-once semantics
            )
            await self._producer.start()
            self._available = True
            logger.info("Kafka producer started.")
        except Exception as e:
            logger.warning("Kafka producer failed to start: %s", e)
            self._available = False

    async def send(self, topic: str, value: dict, key: Optional[str] = None):
        if not self._available or not self._producer:
            return
        try:
            value["_kafka_ts"] = datetime.now(timezone.utc).isoformat()
            await self._producer.send_and_wait(topic, value=value, key=key)
        except Exception as e:
            logger.error("Kafka send failed (%s): %s", topic, e)

    async def send_telemetry(self, entity_id: str, entity_type: str, features: dict):
        await self.send(TOPIC_TELEMETRY, {
            "entity_id":   entity_id,
            "entity_type": entity_type,
            "features":    features,
        }, key=entity_id)

    async def send_anomaly(self, alert: dict):
        await self.send(TOPIC_ANOMALIES, alert, key=alert.get("entity_id"))

    async def send_incident(self, incident: dict):
        await self.send(TOPIC_INCIDENTS, incident, key=incident.get("incident_id"))

    async def stop(self):
        if self._producer:
            await self._producer.stop()
            logger.info("Kafka producer stopped.")


# ─── Consumer ─────────────────────────────────────────────────────────────────

class KafkaConsumer:
    """
    Async Kafka consumer. Runs as a background asyncio task.
    handler: async callable(topic, message_dict) -> None
    """
    def __init__(self, topics: list[str], group_id: str,
                 handler: Callable[[str, dict], asyncio.coroutines]):
        self._topics   = topics
        self._group_id = group_id
        self._handler  = handler
        self._consumer = None
        self._task: Optional[asyncio.Task] = None
        self._running  = False

    async def start(self):
        if not await check_kafka():
            logger.warning("Kafka consumer '%s' not started — broker unavailable.", self._group_id)
            return
        try:
            from aiokafka import AIOKafkaConsumer
            self._consumer = AIOKafkaConsumer(
                *self._topics,
                bootstrap_servers=KAFKA_BOOTSTRAP,
                group_id=self._group_id,
                auto_offset_reset="latest",
                value_deserializer=lambda v: json.loads(v.decode("utf-8")),
                enable_auto_commit=True,
            )
            await self._consumer.start()
            self._running = True
            self._task = asyncio.create_task(self._consume_loop())
            logger.info("Kafka consumer '%s' started on topics: %s", self._group_id, self._topics)
        except Exception as e:
            logger.warning("Kafka consumer failed to start: %s", e)

    async def _consume_loop(self):
        try:
            async for msg in self._consumer:
                if not self._running:
                    break
                try:
                    await self._handler(msg.topic, msg.value)
                except Exception as e:
                    logger.error("Handler error in consumer '%s': %s", self._group_id, e)
        except asyncio.CancelledError:
            pass
        except Exception as e:
            logger.error("Kafka consume loop error: %s", e)

    async def stop(self):
        self._running = False
        if self._task:
            self._task.cancel()
        if self._consumer:
            await self._consumer.stop()
            logger.info("Kafka consumer '%s' stopped.", self._group_id)


# ─── Topic Setup ──────────────────────────────────────────────────────────────

async def ensure_topics():
    """Create required Kafka topics if they don't exist."""
    if not await check_kafka():
        return
    try:
        from kafka.admin import KafkaAdminClient, NewTopic
        admin = KafkaAdminClient(bootstrap_servers=KAFKA_BOOTSTRAP, client_id="cybershield-admin")
        existing = set(admin.list_topics())
        to_create = [
            NewTopic(name=t, num_partitions=3, replication_factor=1)
            for t in ALL_TOPICS if t not in existing
        ]
        if to_create:
            admin.create_topics(to_create)
            logger.info("Created Kafka topics: %s", [t.name for t in to_create])
        admin.close()
    except Exception as e:
        logger.warning("Topic creation failed (non-critical): %s", e)


# ─── Singletons ───────────────────────────────────────────────────────────────

kafka_producer = KafkaProducer()
