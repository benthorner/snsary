# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: test.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n\ntest.proto\x12\x06snsary"Y\n\x07Reading\x12\x0c\n\x04host\x18\x01 \x02(\t\x12\x0e\n\x06sensor\x18\x02 \x02(\t\x12\x0e\n\x06metric\x18\x03 \x02(\t\x12\x11\n\ttimestamp\x18\x04 \x02(\t\x12\r\n\x05value\x18\x05 \x02(\x01'
)


_READING = DESCRIPTOR.message_types_by_name["Reading"]
Reading = _reflection.GeneratedProtocolMessageType(
    "Reading",
    (_message.Message,),
    {
        "DESCRIPTOR": _READING,
        "__module__": "test_pb2"
        # @@protoc_insertion_point(class_scope:snsary.Reading)
    },
)
_sym_db.RegisterMessage(Reading)

if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    _READING._serialized_start = 22
    _READING._serialized_end = 111
# @@protoc_insertion_point(module_scope)
