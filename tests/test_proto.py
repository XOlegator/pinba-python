from pinba.pinba_pb2 import Request


def test_wire_contract():
    expected = [
        ("hostname", 9),
        ("server_name", 9),
        ("script_name", 9),
        ("request_count", 13),
        ("document_size", 13),
        ("memory_peak", 13),
        ("request_time", 2),
        ("ru_utime", 2),
        ("ru_stime", 2),
        ("timer_hit_count", 13),
        ("timer_value", 2),
        ("timer_tag_count", 13),
        ("timer_tag_name", 13),
        ("timer_tag_value", 13),
        ("dictionary", 9),
        ("status", 13),
        ("memory_footprint", 13),
        ("requests", 11),
        ("schema", 9),
        ("tag_name", 13),
        ("tag_value", 13),
        ("timer_ru_utime", 2),
        ("timer_ru_stime", 2),
    ]
    assert [
        (f.name, f.type) for f in sorted(Request.DESCRIPTOR.fields, key=lambda f: f.number)
    ] == expected
    assert [f.number for f in Request.DESCRIPTOR.fields] == list(range(1, 24))
