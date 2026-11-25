"""ASGI HTTP instrumentation through the final body send."""

import random
import socket
from time import perf_counter_ns

from .collector import Collector, current


class PinbaMiddleware:
    def __init__(
        self,
        app,
        reporter,
        *,
        server_name,
        sample_rate=1.0,
        hostname=None,
        max_timers=128,
        max_tag_bytes=256,
    ):
        if not 0 <= sample_rate <= 1:
            raise ValueError("sample_rate must be between 0 and 1")
        self.app, self.reporter, self.server_name = app, reporter, server_name
        self.sample_rate, self.hostname = sample_rate, hostname or socket.gethostname()
        self.max_timers, self.max_tag_bytes = max_timers, max_tag_bytes

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http" or random.random() >= self.sample_rate:
            return await self.app(scope, receive, send)
        collector = Collector(
            self.server_name,
            scope["method"] + " <unmatched>",
            self.hostname,
            self.max_timers,
            self.max_tag_bytes,
        )
        token = current.set(collector)
        finished = False

        def finish(end_ns):
            nonlocal finished
            if finished:
                return
            finished = True
            route = scope.get("route")
            path = getattr(route, "path", None)
            collector.script_name = scope["method"] + " " + (path if path else "<unmatched>")
            self.reporter.submit(collector, end_ns)

        async def wrapped_send(message):
            if message["type"] == "http.response.start":
                collector.status = message["status"]
            if message["type"] == "http.response.body":
                collector.document_size += len(message.get("body", b""))
            await send(message)
            if message["type"] == "http.response.body" and not message.get("more_body", False):
                finish(perf_counter_ns())

        try:
            await self.app(scope, receive, wrapped_send)
        finally:
            try:
                finish(perf_counter_ns())
            finally:
                current.reset(token)
