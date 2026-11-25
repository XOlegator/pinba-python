from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Request(_message.Message):
    __slots__ = ["dictionary", "document_size", "hostname", "memory_footprint", "memory_peak", "request_count", "request_time", "requests", "ru_stime", "ru_utime", "schema", "script_name", "server_name", "status", "tag_name", "tag_value", "timer_hit_count", "timer_ru_stime", "timer_ru_utime", "timer_tag_count", "timer_tag_name", "timer_tag_value", "timer_value"]
    DICTIONARY_FIELD_NUMBER: _ClassVar[int]
    DOCUMENT_SIZE_FIELD_NUMBER: _ClassVar[int]
    HOSTNAME_FIELD_NUMBER: _ClassVar[int]
    MEMORY_FOOTPRINT_FIELD_NUMBER: _ClassVar[int]
    MEMORY_PEAK_FIELD_NUMBER: _ClassVar[int]
    REQUESTS_FIELD_NUMBER: _ClassVar[int]
    REQUEST_COUNT_FIELD_NUMBER: _ClassVar[int]
    REQUEST_TIME_FIELD_NUMBER: _ClassVar[int]
    RU_STIME_FIELD_NUMBER: _ClassVar[int]
    RU_UTIME_FIELD_NUMBER: _ClassVar[int]
    SCHEMA_FIELD_NUMBER: _ClassVar[int]
    SCRIPT_NAME_FIELD_NUMBER: _ClassVar[int]
    SERVER_NAME_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    TAG_NAME_FIELD_NUMBER: _ClassVar[int]
    TAG_VALUE_FIELD_NUMBER: _ClassVar[int]
    TIMER_HIT_COUNT_FIELD_NUMBER: _ClassVar[int]
    TIMER_RU_STIME_FIELD_NUMBER: _ClassVar[int]
    TIMER_RU_UTIME_FIELD_NUMBER: _ClassVar[int]
    TIMER_TAG_COUNT_FIELD_NUMBER: _ClassVar[int]
    TIMER_TAG_NAME_FIELD_NUMBER: _ClassVar[int]
    TIMER_TAG_VALUE_FIELD_NUMBER: _ClassVar[int]
    TIMER_VALUE_FIELD_NUMBER: _ClassVar[int]
    dictionary: _containers.RepeatedScalarFieldContainer[str]
    document_size: int
    hostname: str
    memory_footprint: int
    memory_peak: int
    request_count: int
    request_time: float
    requests: _containers.RepeatedCompositeFieldContainer[Request]
    ru_stime: float
    ru_utime: float
    schema: str
    script_name: str
    server_name: str
    status: int
    tag_name: _containers.RepeatedScalarFieldContainer[int]
    tag_value: _containers.RepeatedScalarFieldContainer[int]
    timer_hit_count: _containers.RepeatedScalarFieldContainer[int]
    timer_ru_stime: _containers.RepeatedScalarFieldContainer[float]
    timer_ru_utime: _containers.RepeatedScalarFieldContainer[float]
    timer_tag_count: _containers.RepeatedScalarFieldContainer[int]
    timer_tag_name: _containers.RepeatedScalarFieldContainer[int]
    timer_tag_value: _containers.RepeatedScalarFieldContainer[int]
    timer_value: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, hostname: _Optional[str] = ..., server_name: _Optional[str] = ..., script_name: _Optional[str] = ..., request_count: _Optional[int] = ..., document_size: _Optional[int] = ..., memory_peak: _Optional[int] = ..., request_time: _Optional[float] = ..., ru_utime: _Optional[float] = ..., ru_stime: _Optional[float] = ..., timer_hit_count: _Optional[_Iterable[int]] = ..., timer_value: _Optional[_Iterable[float]] = ..., timer_tag_count: _Optional[_Iterable[int]] = ..., timer_tag_name: _Optional[_Iterable[int]] = ..., timer_tag_value: _Optional[_Iterable[int]] = ..., dictionary: _Optional[_Iterable[str]] = ..., status: _Optional[int] = ..., memory_footprint: _Optional[int] = ..., requests: _Optional[_Iterable[_Union[Request, _Mapping]]] = ..., schema: _Optional[str] = ..., tag_name: _Optional[_Iterable[int]] = ..., tag_value: _Optional[_Iterable[int]] = ..., timer_ru_utime: _Optional[_Iterable[float]] = ..., timer_ru_stime: _Optional[_Iterable[float]] = ...) -> None: ...
