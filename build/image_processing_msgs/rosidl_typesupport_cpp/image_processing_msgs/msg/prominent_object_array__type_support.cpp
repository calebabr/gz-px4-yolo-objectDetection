// generated from rosidl_typesupport_cpp/resource/idl__type_support.cpp.em
// with input from image_processing_msgs:msg/ProminentObjectArray.idl
// generated code does not contain a copyright notice

#include "cstddef"
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "image_processing_msgs/msg/detail/prominent_object_array__struct.hpp"
#include "rosidl_typesupport_cpp/identifier.hpp"
#include "rosidl_typesupport_cpp/message_type_support.hpp"
#include "rosidl_typesupport_c/type_support_map.h"
#include "rosidl_typesupport_cpp/message_type_support_dispatch.hpp"
#include "rosidl_typesupport_cpp/visibility_control.h"
#include "rosidl_typesupport_interface/macros.h"

namespace image_processing_msgs
{

namespace msg
{

namespace rosidl_typesupport_cpp
{

typedef struct _ProminentObjectArray_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _ProminentObjectArray_type_support_ids_t;

static const _ProminentObjectArray_type_support_ids_t _ProminentObjectArray_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_cpp",  // ::rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
    "rosidl_typesupport_introspection_cpp",  // ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  }
};

typedef struct _ProminentObjectArray_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _ProminentObjectArray_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _ProminentObjectArray_type_support_symbol_names_t _ProminentObjectArray_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, image_processing_msgs, msg, ProminentObjectArray)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, image_processing_msgs, msg, ProminentObjectArray)),
  }
};

typedef struct _ProminentObjectArray_type_support_data_t
{
  void * data[2];
} _ProminentObjectArray_type_support_data_t;

static _ProminentObjectArray_type_support_data_t _ProminentObjectArray_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _ProminentObjectArray_message_typesupport_map = {
  2,
  "image_processing_msgs",
  &_ProminentObjectArray_message_typesupport_ids.typesupport_identifier[0],
  &_ProminentObjectArray_message_typesupport_symbol_names.symbol_name[0],
  &_ProminentObjectArray_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t ProminentObjectArray_message_type_support_handle = {
  ::rosidl_typesupport_cpp::typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_ProminentObjectArray_message_typesupport_map),
  ::rosidl_typesupport_cpp::get_message_typesupport_handle_function,
};

}  // namespace rosidl_typesupport_cpp

}  // namespace msg

}  // namespace image_processing_msgs

namespace rosidl_typesupport_cpp
{

template<>
ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<image_processing_msgs::msg::ProminentObjectArray>()
{
  return &::image_processing_msgs::msg::rosidl_typesupport_cpp::ProminentObjectArray_message_type_support_handle;
}

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_cpp, image_processing_msgs, msg, ProminentObjectArray)() {
  return get_message_type_support_handle<image_processing_msgs::msg::ProminentObjectArray>();
}

#ifdef __cplusplus
}
#endif
}  // namespace rosidl_typesupport_cpp
