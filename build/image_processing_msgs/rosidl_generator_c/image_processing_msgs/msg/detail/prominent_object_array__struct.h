// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from image_processing_msgs:msg/ProminentObjectArray.idl
// generated code does not contain a copyright notice

#ifndef IMAGE_PROCESSING_MSGS__MSG__DETAIL__PROMINENT_OBJECT_ARRAY__STRUCT_H_
#define IMAGE_PROCESSING_MSGS__MSG__DETAIL__PROMINENT_OBJECT_ARRAY__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'objects'
#include "image_processing_msgs/msg/detail/prominent_object__struct.h"

/// Struct defined in msg/ProminentObjectArray in the package image_processing_msgs.
/**
  * ProminentObjectArray.msg
 */
typedef struct image_processing_msgs__msg__ProminentObjectArray
{
  image_processing_msgs__msg__ProminentObject__Sequence objects;
} image_processing_msgs__msg__ProminentObjectArray;

// Struct for a sequence of image_processing_msgs__msg__ProminentObjectArray.
typedef struct image_processing_msgs__msg__ProminentObjectArray__Sequence
{
  image_processing_msgs__msg__ProminentObjectArray * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} image_processing_msgs__msg__ProminentObjectArray__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // IMAGE_PROCESSING_MSGS__MSG__DETAIL__PROMINENT_OBJECT_ARRAY__STRUCT_H_
