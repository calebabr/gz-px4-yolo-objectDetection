// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from image_processing_msgs:msg/DetectionArray.idl
// generated code does not contain a copyright notice

#ifndef IMAGE_PROCESSING_MSGS__MSG__DETAIL__DETECTION_ARRAY__STRUCT_H_
#define IMAGE_PROCESSING_MSGS__MSG__DETAIL__DETECTION_ARRAY__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'detections'
#include "image_processing_msgs/msg/detail/detection__struct.h"

/// Struct defined in msg/DetectionArray in the package image_processing_msgs.
/**
  * DetectionArray.msg
 */
typedef struct image_processing_msgs__msg__DetectionArray
{
  image_processing_msgs__msg__Detection__Sequence detections;
} image_processing_msgs__msg__DetectionArray;

// Struct for a sequence of image_processing_msgs__msg__DetectionArray.
typedef struct image_processing_msgs__msg__DetectionArray__Sequence
{
  image_processing_msgs__msg__DetectionArray * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} image_processing_msgs__msg__DetectionArray__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // IMAGE_PROCESSING_MSGS__MSG__DETAIL__DETECTION_ARRAY__STRUCT_H_
