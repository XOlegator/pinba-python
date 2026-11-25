"""Best-effort non-blocking UDP export; address resolution occurs at startup."""

import socket
from threading import Lock


class Reporter:
    def __init__(self, host: str, port: int, *, max_packet_size: int = 1400):
        if not 1 <= max_packet_size <= 65507:
            raise ValueError("invalid datagram size")
        addresses = socket.getaddrinfo(host, port, type=socket.SOCK_DGRAM)
        family, kind, proto, _, self.address = addresses[0]
        self.socket = socket.socket(family, kind, proto)
        self.socket.setblocking(False)
        self.max_packet_size = max_packet_size
        self.sent = self.errors = self.oversized = self.dropped_timers = 0
        self._lock = Lock()

    def submit(self, collector, end_ns=None):
        try:
            message = collector.finish(end_ns)
            if message is None:
                return False
            data = message.SerializeToString()
            with self._lock:
                self.dropped_timers += collector.dropped_timers
                if len(data) > self.max_packet_size:
                    self.oversized += 1
                    return False
                try:
                    if self.socket.sendto(data, self.address) != len(data):
                        self.errors += 1
                        return False
                except OSError:
                    self.errors += 1
                    return False
                self.sent += 1
                return True
        except ValueError, OverflowError, UnicodeError:
            with self._lock:
                self.errors += 1
            return False

    def close(self):
        self.socket.close()
