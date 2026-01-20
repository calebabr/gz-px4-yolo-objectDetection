// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from image_processing_msgs:msg/ProminentObject.idl
// generated code does not contain a copyright notice

#ifndef IMAGE_PROCESSING_MSGS__MSG__DETAIL__PROMINENT_OBJECT__STRUCT_H_
#define IMAGE_PROCESSING_MSGS__MSG__DETAIL__PROMINENT_OBJECT__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'class_name'
#include "rosidl_runtime_c/string.h"

/// Struct defined in msg/ProminentObject in the package image_processing_msgs.
/**
  * ProminentObject.msg
 */
typedef struct image_processing_msgs__msg__ProminentObject
{
  rosidl_runtime_c__String class_name;
  float x_center;
  float y_center;
  float size_score;
} image_processing_msgs__msg__ProminentObject;

// Struct for a sequence of image_processing_msgs__msg__ProminentObject.
typedef struct image_processing_msgs__msg__ProminentObject__Sequence
{
  image_processing_msgs__msg__ProminentObject * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} image_processing_msgs__msg__ProminentObject__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // IMAGE_PROCESSING_MSGS__MSG__DETAIL__PROMINENT_OBJECT__STRUCT_H_
