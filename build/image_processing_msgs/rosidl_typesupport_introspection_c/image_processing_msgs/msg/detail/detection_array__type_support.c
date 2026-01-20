// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from image_processing_msgs:msg/DetectionArray.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "image_processing_msgs/msg/detail/detection_array__rosidl_typesupport_introspection_c.h"
#include "image_processing_msgs/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "image_processing_msgs/msg/detail/detection_array__functions.h"
#include "image_processing_msgs/msg/detail/detection_array__struct.h"


// Include directives for member types
// Member `detections`
#include "image_processing_msgs/msg/detection.h"
// Member `detections`
#include "image_processing_msgs/msg/detail/detection__rosidl_typesupport_introspection_c.h"

#ifdef __cplusplus
extern "C"
{
#endif

void image_processing_msgs__msg__DetectionArray__rosidl_typesupport_introspection_c__DetectionArray_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  image_processing_msgs__msg__DetectionArray__init(message_memory);
}

void image_processing_msgs__msg__DetectionArray__rosidl_typesupport_introspection_c__DetectionArray_fini_function(void * message_memory)
{
  image_processing_msgs__msg__DetectionArray__fini(message_memory);
}

size_t image_processing_msgs__msg__DetectionArray__rosidl_typesupport_introspection_c__size_function__DetectionArray__detections(
  const void * untyped_member)
{
  const image_processing_msgs__msg__Detection__Sequence * member =
    (const image_processing_msgs__msg__Detection__Sequence *)(untyped_member);
  return member->size;
}

const void * image_processing_msgs__msg__DetectionArray__rosidl_typesupport_introspection_c__get_const_function__DetectionArray__detections(
  const void * untyped_member, size_t index)
{
  const image_processing_msgs__msg__Detection__Sequence * member =
    (const image_processing_msgs__msg__Detection__Sequence *)(untyped_member);
  return &member->data[index];
}

void * image_processing_msgs__msg__DetectionArray__rosidl_typesupport_introspection_c__get_function__DetectionArray__detections(
  void * untyped_member, size_t index)
{
  image_processing_msgs__msg__Detection__Sequence * member =
    (image_processing_msgs__msg__Detection__Sequence *)(untyped_member);
  return &member->data[index];
}

void image_processing_msgs__msg__DetectionArray__rosidl_typesupport_introspection_c__fetch_function__DetectionArray__detections(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const image_processing_msgs__msg__Detection * item =
    ((const image_processing_msgs__msg__Detection *)
    image_processing_msgs__msg__DetectionArray__rosidl_typesupport_introspection_c__get_const_function__DetectionArray__detections(untyped_member, index));
  image_processing_msgs__msg__Detection * value =
    (image_processing_msgs__msg__Detection *)(untyped_value);
  *value = *item;
}

void image_processing_msgs__msg__DetectionArray__rosidl_typesupport_introspection_c__assign_function__DetectionArray__detections(
  void * untyped_member, size_t index, const void * untyped_value)
{
  image_processing_msgs__msg__Detection * item =
    ((image_processing_msgs__msg__Detection *)
    image_processing_msgs__msg__DetectionArray__rosidl_typesupport_introspection_c__get_function__DetectionArray__detections(untyped_member, index));
  const image_processing_msgs__msg__Detection * value =
    (const image_processing_msgs__msg__Detection *)(untyped_value);
  *item = *value;
}

bool image_processing_msgs__msg__DetectionArray__rosidl_typesupport_introspection_c__resize_function__DetectionArray__detections(
  void * untyped_member, size_t size)
{
  image_processing_msgs__msg__Detection__Sequence * member =
    (image_processing_msgs__msg__Detection__Sequence *)(untyped_member);
  image_processing_msgs__msg__Detection__Sequence__fini(member);
  return image_processing_msgs__msg__Detection__Sequence__init(member, size);
}

static rosidl_typesupport_introspection_c__MessageMember image_processing_msgs__msg__DetectionArray__rosidl_typesupport_introspection_c__DetectionArray_message_member_array[1] = {
  {
    "detections",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(image_processing_msgs__msg__DetectionArray, detections),  // bytes offset in struct
    NULL,  // default value
    image_processing_msgs__msg__DetectionArray__rosidl_typesupport_introspection_c__size_function__DetectionArray__detections,  // size() function pointer
    image_processing_msgs__msg__DetectionArray__rosidl_typesupport_introspection_c__get_const_function__DetectionArray__detections,  // get_const(index) function pointer
    image_processing_msgs__msg__DetectionArray__rosidl_typesupport_introspection_c__get_function__DetectionArray__detections,  // get(index) function pointer
    image_processing_msgs__msg__DetectionArray__rosidl_typesupport_introspection_c__fetch_function__DetectionArray__detections,  // fetch(index, &value) function pointer
    image_processing_msgs__msg__DetectionArray__rosidl_typesupport_introspection_c__assign_function__DetectionArray__detections,  // assign(index, value) function pointer
    image_processing_msgs__msg__DetectionArray__rosidl_typesupport_introspection_c__resize_function__DetectionArray__detections  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers image_processing_msgs__msg__DetectionArray__rosidl_typesupport_introspection_c__DetectionArray_message_members = {
  "image_processing_msgs__msg",  // message namespace
  "DetectionArray",  // message name
  1,  // number of fields
  sizeof(image_processing_msgs__msg__DetectionArray),
  image_processing_msgs__msg__DetectionArray__rosidl_typesupport_introspection_c__DetectionArray_message_member_array,  // message members
  image_processing_msgs__msg__DetectionArray__rosidl_typesupport_introspection_c__DetectionArray_init_function,  // function to initialize message memory (memory has to be allocated)
  image_processing_msgs__msg__DetectionArray__rosidl_typesupport_introspection_c__DetectionArray_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t image_processing_msgs__msg__DetectionArray__rosidl_typesupport_introspection_c__DetectionArray_message_type_support_handle = {
  0,
  &image_processing_msgs__msg__DetectionArray__rosidl_typesupport_introspection_c__DetectionArray_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_image_processing_msgs
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, image_processing_msgs, msg, DetectionArray)() {
  image_processing_msgs__msg__DetectionArray__rosidl_typesupport_introspection_c__DetectionArray_message_member_array[0].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, image_processing_msgs, msg, Detection)();
  if (!image_processing_msgs__msg__DetectionArray__rosidl_typesupport_introspection_c__DetectionArray_message_type_support_handle.typesupport_identifier) {
    image_processing_msgs__msg__DetectionArray__rosidl_typesupport_introspection_c__DetectionArray_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &image_processing_msgs__msg__DetectionArray__rosidl_typesupport_introspection_c__DetectionArray_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif
