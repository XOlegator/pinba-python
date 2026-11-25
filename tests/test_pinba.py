import asyncio
import socket
from concurrent.futures import ThreadPoolExecutor
from contextvars import copy_context

import pytest

from pinba import Collector, PinbaMiddleware, Reporter, record
from pinba.pinba_pb2 import Request


def test_dictionary_and_parallel_arrays():
    c = Collector("api", "GET /test", "host", tags={"group": "ai_naming"})
    c.record(0.01, {"group": "ai_naming", "category": "naming.registry"})
    c.record(0.02, {"group": "ai_naming", "category": "имя"})
    packet = Request.FromString(c.finish().SerializeToString())
    assert packet.IsInitialized() and packet.request_count == 1
    assert packet.timer_hit_count == [1, 1]
    assert packet.timer_tag_count == [2, 2]
    assert len(packet.timer_tag_name) == len(packet.timer_tag_value) == 4
    assert [
        (packet.dictionary[n], packet.dictionary[v])
        for n, v in zip(packet.timer_tag_name, packet.timer_tag_value, strict=True)
    ] == [
        ("group", "ai_naming"),
        ("category", "naming.registry"),
        ("group", "ai_naming"),
        ("category", "имя"),
    ]
    assert [
        (packet.dictionary[n], packet.dictionary[v])
        for n, v in zip(packet.tag_name, packet.tag_value, strict=True)
    ] == [("group", "ai_naming")]
    assert packet.memory_peak == packet.ru_utime == packet.ru_stime == 0
    assert not c.record(0.1, {"a": "b"})


def test_udp_and_limits():
    receiver = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    receiver.bind(("127.0.0.1", 0))
    receiver.settimeout(1)
    reporter = Reporter("127.0.0.1", receiver.getsockname()[1])
    c = Collector("api", "task", "host", max_timers=1)
    assert c.record(0.1, {"a": "b"})
    assert not c.record(0.2, {"a": "c"})
    assert reporter.submit(c)
    assert Request.FromString(receiver.recv(65535)).IsInitialized()
    assert reporter.sent == reporter.dropped_timers == 1
    reporter.close()
    receiver.close()
    reporter = Reporter("127.0.0.1", 12345, max_packet_size=1)
    assert not reporter.submit(Collector("api", "task", "host"))
    assert reporter.oversized == 1
    reporter.close()


def test_asgi_isolation_thread_and_late_tasks():
    class Capture:
        def __init__(self):
            self.packets = []

        def submit(self, collector, end_ns=None):
            self.packets.append(collector.finish(end_ns))

    capture = Capture()
    late = []

    async def app(scope, receive, send):
        scope["route"] = type("Route", (), {"path": "/items/{id}"})()
        context = copy_context()
        with ThreadPoolExecutor() as pool:
            assert await asyncio.get_running_loop().run_in_executor(
                pool, context.run, record, 0.01, {"category": scope["id"]}
            )

        async def background():
            await asyncio.sleep(0.02)
            return record(0.01, {"category": "late"})

        late.append(asyncio.create_task(background()))
        await asyncio.sleep(0.001)
        await send({"type": "http.response.start", "status": 201})
        await send({"type": "http.response.body", "body": b"abc", "more_body": True})
        await send({"type": "http.response.body", "body": b"de"})

    middleware = PinbaMiddleware(app, capture, server_name="api")

    async def run():
        async def send(message):
            pass

        await asyncio.gather(
            *(
                middleware({"type": "http", "method": "GET", "id": str(i)}, None, send)
                for i in range(10)
            )
        )
        assert not any(await asyncio.gather(*late))

    asyncio.run(run())
    assert len(capture.packets) == 10
    assert {p.dictionary[p.timer_tag_value[0]] for p in capture.packets} == {
        str(i) for i in range(10)
    }
    assert all(
        p.status == 201 and p.document_size == 5 and p.script_name == "GET /items/{id}"
        for p in capture.packets
    )


def test_exception_finishes():
    packets = []

    class Capture:
        def submit(self, collector, end_ns=None):
            packets.append(collector.finish(end_ns))

    async def app(scope, receive, send):
        raise RuntimeError("failure")

    async def run():
        with pytest.raises(RuntimeError):
            await PinbaMiddleware(app, Capture(), server_name="api")(
                {"type": "http", "method": "GET"}, None, None
            )

    asyncio.run(run())
    assert len(packets) == 1
