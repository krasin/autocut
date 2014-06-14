# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: config.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)




DESCRIPTOR = _descriptor.FileDescriptor(
  name='config.proto',
  package='config',
  serialized_pb='\n\x0c\x63onfig.proto\x12\x06\x63onfig\"\xcd\x02\n\x06\x43onfig\x12\x0b\n\x03top\x18\x01 \x01(\x02\x12\x0e\n\x06\x62ottom\x18\x02 \x01(\x02\x12\x14\n\tstep_down\x18\x03 \x01(\x02:\x01\x31\x12\x14\n\tstep_over\x18\x04 \x01(\x02:\x01\x32\x12 \n\x12vertical_tolerance\x18\x05 \x01(\x02:\x04\x30.05\x12\x1c\n\rtool_diameter\x18\x06 \x01(\x02:\x05\x33.175\x12\x18\n\x10\x63learance_height\x18\x07 \x01(\x02\x12\x13\n\x0b\x66\x65\x65\x64_height\x18\x08 \x01(\x02\x12\x0c\n\x04\x66\x65\x65\x64\x18\t \x01(\x02\x12\x13\n\x0bplunge_feed\x18\n \x01(\x02\x12\x13\n\x08rotate_x\x18\x0b \x01(\x02:\x01\x30\x12\x13\n\x08rotate_y\x18\x0c \x01(\x02:\x01\x30\x12\x13\n\x08rotate_z\x18\r \x01(\x02:\x01\x30\x12\x13\n\x0bin_filename\x18\x0e \x01(\t\x12\x14\n\x0cout_filename\x18\x0f \x01(\t')




_CONFIG = _descriptor.Descriptor(
  name='Config',
  full_name='config.Config',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='top', full_name='config.Config.top', index=0,
      number=1, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='bottom', full_name='config.Config.bottom', index=1,
      number=2, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='step_down', full_name='config.Config.step_down', index=2,
      number=3, type=2, cpp_type=6, label=1,
      has_default_value=True, default_value=1,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='step_over', full_name='config.Config.step_over', index=3,
      number=4, type=2, cpp_type=6, label=1,
      has_default_value=True, default_value=2,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='vertical_tolerance', full_name='config.Config.vertical_tolerance', index=4,
      number=5, type=2, cpp_type=6, label=1,
      has_default_value=True, default_value=0.05,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='tool_diameter', full_name='config.Config.tool_diameter', index=5,
      number=6, type=2, cpp_type=6, label=1,
      has_default_value=True, default_value=3.175,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='clearance_height', full_name='config.Config.clearance_height', index=6,
      number=7, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='feed_height', full_name='config.Config.feed_height', index=7,
      number=8, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='feed', full_name='config.Config.feed', index=8,
      number=9, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='plunge_feed', full_name='config.Config.plunge_feed', index=9,
      number=10, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='rotate_x', full_name='config.Config.rotate_x', index=10,
      number=11, type=2, cpp_type=6, label=1,
      has_default_value=True, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='rotate_y', full_name='config.Config.rotate_y', index=11,
      number=12, type=2, cpp_type=6, label=1,
      has_default_value=True, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='rotate_z', full_name='config.Config.rotate_z', index=12,
      number=13, type=2, cpp_type=6, label=1,
      has_default_value=True, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='in_filename', full_name='config.Config.in_filename', index=13,
      number=14, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='out_filename', full_name='config.Config.out_filename', index=14,
      number=15, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=25,
  serialized_end=358,
)

DESCRIPTOR.message_types_by_name['Config'] = _CONFIG

class Config(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _CONFIG

  # @@protoc_insertion_point(class_scope:config.Config)


# @@protoc_insertion_point(module_scope)