# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: proto/full.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x10proto/full.proto\x12\x06jparty\"_\n\x08Question\x12\x0c\n\x04text\x18\x01 \x02(\t\x12\x0e\n\x06\x61nswer\x18\x02 \x02(\t\x12\r\n\x05value\x18\x03 \x01(\x05\x12\x14\n\x0c\x64\x61ily_double\x18\x04 \x01(\x08\x12\x10\n\x08\x63omplete\x18\x05 \x01(\x08\"Z\n\x08\x43\x61tegory\x12\x0c\n\x04name\x18\x01 \x02(\t\x12#\n\tquestions\x18\x02 \x03(\x0b\x32\x10.jparty.Question\x12\x1b\n\x13\x64\x65\x66\x61ult_start_value\x18\x03 \x01(\x05\"J\n\x05\x42oard\x12$\n\ncategories\x18\x01 \x03(\x0b\x32\x10.jparty.Category\x12\x1b\n\x13\x64\x65\x66\x61ult_start_value\x18\x02 \x01(\x05\"}\n\x08GameData\x12\r\n\x05title\x18\x01 \x02(\t\x12\x0c\n\x04\x64\x61te\x18\x02 \x01(\t\x12\x1b\n\x13\x64\x65\x66\x61ult_start_value\x18\x03 \x01(\x05\x12\x18\n\x10round_multiplier\x18\x04 \x01(\x05\x12\x1d\n\x06rounds\x18\x05 \x03(\x0b\x32\r.jparty.Board')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'proto.full_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _QUESTION._serialized_start=28
  _QUESTION._serialized_end=123
  _CATEGORY._serialized_start=125
  _CATEGORY._serialized_end=215
  _BOARD._serialized_start=217
  _BOARD._serialized_end=291
  _GAMEDATA._serialized_start=293
  _GAMEDATA._serialized_end=418
# @@protoc_insertion_point(module_scope)
