// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from image_processing_msgs:msg/ProminentObject.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "image_processing_msgs/msg/detail/prominent_object__rosidl_typesupport_introspection_c.h"
#include "image_processing_msgs/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "image_processing_msgs/msg/detail/prominent_object__functions.h"
#include "image_processing_msgs/msg/detail/prominent_object__struct.h"


// Include directives for member types
// Member `class_name`
#include "rosidl_runtime_c/string_functions.h"

#ifdef __cplusplus
extern "C"
{
#endif

void image_processing_msgs__msg__ProminentObject__rosidl_typesupport_introspection_c__ProminentObject_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  image_processing_msgs__msg__ProminentObject__init(message_memory);
}

void image_processing_msgs__msg__ProminentObject__rosidl_typesupport_introspection_c__ProminentObject_fini_function(void * message_memory)
{
  image_processing_msgs__msg__ProminentObject__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember image_processing_msgs__msg__ProminentObject__rosidl_typesupport_introspection_c__ProminentObject_message_member_array[4] = {
  {
    "class_name",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(image_processing_msgs__msg__ProminentObject, class_name),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "x_center",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(image_processing_msgs__msg__ProminentObject, x_center),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "y_center",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(image_processing_msgs__msg__ProminentObject, y_center),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "size_score",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(image_processing_msgs__msg__ProminentObject, size_score),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers image_processing_msgs__msg__ProminentObject__rosidl_typesupport_introspection_c__ProminentObject_message_members = {
  "image_processing_msgs__msg",  // message namespace
  "ProminentObject",  // message name
  4,  // number of fields
  sizeof(image_processing_msgs__msg__ProminentObject),
  image_processing_msgs__msg__ProminentObject__rosidl_typesupport_introspection_c__ProminentObject_message_member_array,  // message members
  image_processing_msgs__msg__ProminentObject__rosidl_typesupport_introspection_c__ProminentObject_init_function,  // function to initialize message memory (memory has to be allocated)
  image_processing_msgs__msg__ProminentObject__rosidl_typesupport_introspection_c__ProminentObject_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t image_processing_msgs__msg__ProminentObject__rosidl_typesupport_introspection_c__ProminentObject_message_type_support_handle = {
  0,
  &image_processing_msgs__msg__ProminentObject__rosidl_typesupport_introspection_c__ProminentObject_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_image_processing_msgs
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, image_processing_msgs, msg, ProminentObject)() {
  if (!image_processing_msgs__msg__ProminentObject__rosidl_typesupport_introspection_c__ProminentObject_message_type_support_handle.typesupport_identifier) {
    image_processing_msgs__msg__ProminentObject__rosidl_typesupport_introspection_c__ProminentObject_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &image_processing_msgs__msg__ProminentObject__rosidl_typesupport_introspection_c__ProminentObject_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif
