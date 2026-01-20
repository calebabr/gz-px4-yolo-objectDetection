// generated from rosidl_generator_c/resource/idl__functions.h.em
// with input from image_processing_msgs:msg/ProminentObjectArray.idl
// generated code does not contain a copyright notice

#ifndef IMAGE_PROCESSING_MSGS__MSG__DETAIL__PROMINENT_OBJECT_ARRAY__FUNCTIONS_H_
#define IMAGE_PROCESSING_MSGS__MSG__DETAIL__PROMINENT_OBJECT_ARRAY__FUNCTIONS_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stdlib.h>

#include "rosidl_runtime_c/visibility_control.h"
#include "image_processing_msgs/msg/rosidl_generator_c__visibility_control.h"

#include "image_processing_msgs/msg/detail/prominent_object_array__struct.h"

/// Initialize msg/ProminentObjectArray message.
/**
 * If the init function is called twice for the same message without
 * calling fini inbetween previously allocated memory will be leaked.
 * \param[in,out] msg The previously allocated message pointer.
 * Fields without a default value will not be initialized by this function.
 * You might want to call memset(msg, 0, sizeof(
 * image_processing_msgs__msg__ProminentObjectArray
 * )) before or use
 * image_processing_msgs__msg__ProminentObjectArray__create()
 * to allocate and initialize the message.
 * \return true if initialization was successful, otherwise false
 */
ROSIDL_GENERATOR_C_PUBLIC_image_processing_msgs
bool
image_processing_msgs__msg__ProminentObjectArray__init(image_processing_msgs__msg__ProminentObjectArray * msg);

/// Finalize msg/ProminentObjectArray message.
/**
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_image_processing_msgs
void
image_processing_msgs__msg__ProminentObjectArray__fini(image_processing_msgs__msg__ProminentObjectArray * msg);

/// Create msg/ProminentObjectArray message.
/**
 * It allocates the memory for the message, sets the memory to zero, and
 * calls
 * image_processing_msgs__msg__ProminentObjectArray__init().
 * \return The pointer to the initialized message if successful,
 * otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_image_processing_msgs
image_processing_msgs__msg__ProminentObjectArray *
image_processing_msgs__msg__ProminentObjectArray__create();

/// Destroy msg/ProminentObjectArray message.
/**
 * It calls
 * image_processing_msgs__msg__ProminentObjectArray__fini()
 * and frees the memory of the message.
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_image_processing_msgs
void
image_processing_msgs__msg__ProminentObjectArray__destroy(image_processing_msgs__msg__ProminentObjectArray * msg);

/// Check for msg/ProminentObjectArray message equality.
/**
 * \param[in] lhs The message on the left hand size of the equality operator.
 * \param[in] rhs The message on the right hand size of the equality operator.
 * \return true if messages are equal, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_image_processing_msgs
bool
image_processing_msgs__msg__ProminentObjectArray__are_equal(const image_processing_msgs__msg__ProminentObjectArray * lhs, const image_processing_msgs__msg__ProminentObjectArray * rhs);

/// Copy a msg/ProminentObjectArray message.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source message pointer.
 * \param[out] output The target message pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer is null
 *   or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_image_processing_msgs
bool
image_processing_msgs__msg__ProminentObjectArray__copy(
  const image_processing_msgs__msg__ProminentObjectArray * input,
  image_processing_msgs__msg__ProminentObjectArray * output);

/// Initialize array of msg/ProminentObjectArray messages.
/**
 * It allocates the memory for the number of elements and calls
 * image_processing_msgs__msg__ProminentObjectArray__init()
 * for each element of the array.
 * \param[in,out] array The allocated array pointer.
 * \param[in] size The size / capacity of the array.
 * \return true if initialization was successful, otherwise false
 * If the array pointer is valid and the size is zero it is guaranteed
 # to return true.
 */
ROSIDL_GENERATOR_C_PUBLIC_image_processing_msgs
bool
image_processing_msgs__msg__ProminentObjectArray__Sequence__init(image_processing_msgs__msg__ProminentObjectArray__Sequence * array, size_t size);

/// Finalize array of msg/ProminentObjectArray messages.
/**
 * It calls
 * image_processing_msgs__msg__ProminentObjectArray__fini()
 * for each element of the array and frees the memory for the number of
 * elements.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_image_processing_msgs
void
image_processing_msgs__msg__ProminentObjectArray__Sequence__fini(image_processing_msgs__msg__ProminentObjectArray__Sequence * array);

/// Create array of msg/ProminentObjectArray messages.
/**
 * It allocates the memory for the array and calls
 * image_processing_msgs__msg__ProminentObjectArray__Sequence__init().
 * \param[in] size The size / capacity of the array.
 * \return The pointer to the initialized array if successful, otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_image_processing_msgs
image_processing_msgs__msg__ProminentObjectArray__Sequence *
image_processing_msgs__msg__ProminentObjectArray__Sequence__create(size_t size);

/// Destroy array of msg/ProminentObjectArray messages.
/**
 * It calls
 * image_processing_msgs__msg__ProminentObjectArray__Sequence__fini()
 * on the array,
 * and frees the memory of the array.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_image_processing_msgs
void
image_processing_msgs__msg__ProminentObjectArray__Sequence__destroy(image_processing_msgs__msg__ProminentObjectArray__Sequence * array);

/// Check for msg/ProminentObjectArray message array equality.
/**
 * \param[in] lhs The message array on the left hand size of the equality operator.
 * \param[in] rhs The message array on the right hand size of the equality operator.
 * \return true if message arrays are equal in size and content, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_image_processing_msgs
bool
image_processing_msgs__msg__ProminentObjectArray__Sequence__are_equal(const image_processing_msgs__msg__ProminentObjectArray__Sequence * lhs, const image_processing_msgs__msg__ProminentObjectArray__Sequence * rhs);

/// Copy an array of msg/ProminentObjectArray messages.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source array pointer.
 * \param[out] output The target array pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer
 *   is null or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_image_processing_msgs
bool
image_processing_msgs__msg__ProminentObjectArray__Sequence__copy(
  const image_processing_msgs__msg__ProminentObjectArray__Sequence * input,
  image_processing_msgs__msg__ProminentObjectArray__Sequence * output);

#ifdef __cplusplus
}
#endif

#endif  // IMAGE_PROCESSING_MSGS__MSG__DETAIL__PROMINENT_OBJECT_ARRAY__FUNCTIONS_H_
