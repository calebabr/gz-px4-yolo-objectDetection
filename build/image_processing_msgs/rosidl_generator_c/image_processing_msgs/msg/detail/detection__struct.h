// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from image_processing_msgs:msg/Detection.idl
// generated code does not contain a copyright notice

#ifndef IMAGE_PROCESSING_MSGS__MSG__DETAIL__DETECTION__STRUCT_H_
#define IMAGE_PROCESSING_MSGS__MSG__DETAIL__DETECTION__STRUCT_H_

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

/// Struct defined in msg/Detection in the package image_processing_msgs.
/**
  * Detection.msg
 */
typedef struct image_processing_msgs__msg__Detection
{
  rosidl_runtime_c__String class_name;
  float confidence;
  float x_min;
  float y_min;
  float x_max;
  float y_max;
  float x_center;
  float y_center;
  float width;
  float height;
  float pixel_area;
} image_processing_msgs__msg__Detection;

// Struct for a sequence of image_processing_msgs__msg__Detection.
typedef struct image_processing_msgs__msg__Detection__Sequence
{
  image_processing_msgs__msg__Detection * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} image_processing_msgs__msg__Detection__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // IMAGE_PROCESSING_MSGS__MSG__DETAIL__DETECTION__STRUCT_H_
