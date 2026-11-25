"""Request-local collection, including calls from copied thread contexts."""

import math
from collections.abc import Mapping
from contextlib import contextmanager
from contextvars import ContextVar
from dataclasses import dataclass, field
from threading import Lock
from time import perf_counter_ns

from . import pinba_pb2

current: ContextVar[Collector | None] = ContextVar("pinba_current", default=None)


@dataclass
class Collector:
    server_name: str
    script_name: str
    hostname: str
    max_timers: int = 128
    max_tag_bytes: int = 256
    tags: Mapping[str, str] = field(default_factory=dict)
    start_ns: int = field(default_factory=perf_counter_ns)
    status: int = 0
    document_size: int = 0
    _timers: list = field(default_factory=list, init=False)
    _lock: Lock = field(default_factory=Lock, init=False)
    _closed: bool = field(default=False, init=False)
    dropped_timers: int = field(default=0, init=False)

    def _validate_tags(self, tags):
        return all(
            isinstance(k, str)
            and isinstance(v, str)
            and k
            and v
            and len(k.encode("utf-8")) <= self.max_tag_bytes
            and len(v.encode("utf-8")) <= self.max_tag_bytes
            for k, v in tags.items()
        )

    def record(self, seconds: float, tags: Mapping[str, str]) -> bool:
        if not math.isfinite(seconds) or seconds < 0 or seconds > 3.4e38:
            return False
        tags = dict(tags)
        with self._lock:
            if self._closed:
                return False
            if len(self._timers) >= self.max_timers or not tags or not self._validate_tags(tags):
                self.dropped_timers += 1
                return False
            self._timers.append((seconds, tags))
            return True

    @contextmanager
    def timed_block(self, tags: Mapping[str, str]):
        start = perf_counter_ns()
        try:
            yield
        finally:
            self.record((perf_counter_ns() - start) / 1e9, tags)

    def finish(self, end_ns: int | None = None):
        """Close collection and build a protobuf once; late writes are ignored."""
        with self._lock:
            if self._closed:
                return None
            self._closed = True
            timers = self._timers[:]
            tags = dict(self.tags)
        if not self._validate_tags(tags):
            raise ValueError("invalid request tags")
        request = pinba_pb2.Request(
            hostname=self.hostname,
            server_name=self.server_name,
            script_name=self.script_name,
            request_count=1,
            document_size=min(self.document_size, 2**32 - 1),
            memory_peak=0,
            request_time=max(
                0, (end_ns if end_ns is not None else perf_counter_ns()) - self.start_ns
            )
            / 1e9,
            ru_utime=0,
            ru_stime=0,
        )
        if self.status:
            request.status = self.status
        dictionary = {}

        def index(word):
            if word not in dictionary:
                dictionary[word] = len(dictionary)
                request.dictionary.append(word)
            return dictionary[word]

        for name, value in tags.items():
            request.tag_name.append(index(name))
            request.tag_value.append(index(value))
        for seconds, timer_tags in timers:
            request.timer_hit_count.append(1)
            request.timer_value.append(seconds)
            request.timer_tag_count.append(len(timer_tags))
            for name, value in timer_tags.items():
                request.timer_tag_name.append(index(name))
                request.timer_tag_value.append(index(value))
        return request

    @contextmanager
    def activate(self, reporter):
        token = current.set(self)
        try:
            yield self
        finally:
            current.reset(token)
            reporter.submit(self)


def record(seconds: float, tags: Mapping[str, str]) -> bool:
    collector = current.get()
    return collector.record(seconds, tags) if collector else False


@contextmanager
def timed_block(tags: Mapping[str, str]):
    collector = current.get()
    if collector is None:
        yield
    else:
        with collector.timed_block(tags):
            yield
