// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from image_processing_msgs:msg/ProminentObjectArray.idl
// generated code does not contain a copyright notice
#include "image_processing_msgs/msg/detail/prominent_object_array__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `objects`
#include "image_processing_msgs/msg/detail/prominent_object__functions.h"

bool
image_processing_msgs__msg__ProminentObjectArray__init(image_processing_msgs__msg__ProminentObjectArray * msg)
{
  if (!msg) {
    return false;
  }
  // objects
  if (!image_processing_msgs__msg__ProminentObject__Sequence__init(&msg->objects, 0)) {
    image_processing_msgs__msg__ProminentObjectArray__fini(msg);
    return false;
  }
  return true;
}

void
image_processing_msgs__msg__ProminentObjectArray__fini(image_processing_msgs__msg__ProminentObjectArray * msg)
{
  if (!msg) {
    return;
  }
  // objects
  image_processing_msgs__msg__ProminentObject__Sequence__fini(&msg->objects);
}

bool
image_processing_msgs__msg__ProminentObjectArray__are_equal(const image_processing_msgs__msg__ProminentObjectArray * lhs, const image_processing_msgs__msg__ProminentObjectArray * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // objects
  if (!image_processing_msgs__msg__ProminentObject__Sequence__are_equal(
      &(lhs->objects), &(rhs->objects)))
  {
    return false;
  }
  return true;
}

bool
image_processing_msgs__msg__ProminentObjectArray__copy(
  const image_processing_msgs__msg__ProminentObjectArray * input,
  image_processing_msgs__msg__ProminentObjectArray * output)
{
  if (!input || !output) {
    return false;
  }
  // objects
  if (!image_processing_msgs__msg__ProminentObject__Sequence__copy(
      &(input->objects), &(output->objects)))
  {
    return false;
  }
  return true;
}

image_processing_msgs__msg__ProminentObjectArray *
image_processing_msgs__msg__ProminentObjectArray__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  image_processing_msgs__msg__ProminentObjectArray * msg = (image_processing_msgs__msg__ProminentObjectArray *)allocator.allocate(sizeof(image_processing_msgs__msg__ProminentObjectArray), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(image_processing_msgs__msg__ProminentObjectArray));
  bool success = image_processing_msgs__msg__ProminentObjectArray__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
image_processing_msgs__msg__ProminentObjectArray__destroy(image_processing_msgs__msg__ProminentObjectArray * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    image_processing_msgs__msg__ProminentObjectArray__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
image_processing_msgs__msg__ProminentObjectArray__Sequence__init(image_processing_msgs__msg__ProminentObjectArray__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  image_processing_msgs__msg__ProminentObjectArray * data = NULL;

  if (size) {
    data = (image_processing_msgs__msg__ProminentObjectArray *)allocator.zero_allocate(size, sizeof(image_processing_msgs__msg__ProminentObjectArray), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = image_processing_msgs__msg__ProminentObjectArray__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        image_processing_msgs__msg__ProminentObjectArray__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
image_processing_msgs__msg__ProminentObjectArray__Sequence__fini(image_processing_msgs__msg__ProminentObjectArray__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      image_processing_msgs__msg__ProminentObjectArray__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

image_processing_msgs__msg__ProminentObjectArray__Sequence *
image_processing_msgs__msg__ProminentObjectArray__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  image_processing_msgs__msg__ProminentObjectArray__Sequence * array = (image_processing_msgs__msg__ProminentObjectArray__Sequence *)allocator.allocate(sizeof(image_processing_msgs__msg__ProminentObjectArray__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = image_processing_msgs__msg__ProminentObjectArray__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
image_processing_msgs__msg__ProminentObjectArray__Sequence__destroy(image_processing_msgs__msg__ProminentObjectArray__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    image_processing_msgs__msg__ProminentObjectArray__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
image_processing_msgs__msg__ProminentObjectArray__Sequence__are_equal(const image_processing_msgs__msg__ProminentObjectArray__Sequence * lhs, const image_processing_msgs__msg__ProminentObjectArray__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!image_processing_msgs__msg__ProminentObjectArray__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
image_processing_msgs__msg__ProminentObjectArray__Sequence__copy(
  const image_processing_msgs__msg__ProminentObjectArray__Sequence * input,
  image_processing_msgs__msg__ProminentObjectArray__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(image_processing_msgs__msg__ProminentObjectArray);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    image_processing_msgs__msg__ProminentObjectArray * data =
      (image_processing_msgs__msg__ProminentObjectArray *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!image_processing_msgs__msg__ProminentObjectArray__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          image_processing_msgs__msg__ProminentObjectArray__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!image_processing_msgs__msg__ProminentObjectArray__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
