// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from image_processing_msgs:msg/ProminentObjectArray.idl
// generated code does not contain a copyright notice

#ifndef IMAGE_PROCESSING_MSGS__MSG__DETAIL__PROMINENT_OBJECT_ARRAY__STRUCT_HPP_
#define IMAGE_PROCESSING_MSGS__MSG__DETAIL__PROMINENT_OBJECT_ARRAY__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


// Include directives for member types
// Member 'objects'
#include "image_processing_msgs/msg/detail/prominent_object__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__image_processing_msgs__msg__ProminentObjectArray __attribute__((deprecated))
#else
# define DEPRECATED__image_processing_msgs__msg__ProminentObjectArray __declspec(deprecated)
#endif

namespace image_processing_msgs
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct ProminentObjectArray_
{
  using Type = ProminentObjectArray_<ContainerAllocator>;

  explicit ProminentObjectArray_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_init;
  }

  explicit ProminentObjectArray_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_init;
    (void)_alloc;
  }

  // field types and members
  using _objects_type =
    std::vector<image_processing_msgs::msg::ProminentObject_<ContainerAllocator>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<image_processing_msgs::msg::ProminentObject_<ContainerAllocator>>>;
  _objects_type objects;

  // setters for named parameter idiom
  Type & set__objects(
    const std::vector<image_processing_msgs::msg::ProminentObject_<ContainerAllocator>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<image_processing_msgs::msg::ProminentObject_<ContainerAllocator>>> & _arg)
  {
    this->objects = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    image_processing_msgs::msg::ProminentObjectArray_<ContainerAllocator> *;
  using ConstRawPtr =
    const image_processing_msgs::msg::ProminentObjectArray_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<image_processing_msgs::msg::ProminentObjectArray_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<image_processing_msgs::msg::ProminentObjectArray_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      image_processing_msgs::msg::ProminentObjectArray_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<image_processing_msgs::msg::ProminentObjectArray_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      image_processing_msgs::msg::ProminentObjectArray_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<image_processing_msgs::msg::ProminentObjectArray_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<image_processing_msgs::msg::ProminentObjectArray_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<image_processing_msgs::msg::ProminentObjectArray_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__image_processing_msgs__msg__ProminentObjectArray
    std::shared_ptr<image_processing_msgs::msg::ProminentObjectArray_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__image_processing_msgs__msg__ProminentObjectArray
    std::shared_ptr<image_processing_msgs::msg::ProminentObjectArray_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const ProminentObjectArray_ & other) const
  {
    if (this->objects != other.objects) {
      return false;
    }
    return true;
  }
  bool operator!=(const ProminentObjectArray_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct ProminentObjectArray_

// alias to use template instance with default allocator
using ProminentObjectArray =
  image_processing_msgs::msg::ProminentObjectArray_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace image_processing_msgs

#endif  // IMAGE_PROCESSING_MSGS__MSG__DETAIL__PROMINENT_OBJECT_ARRAY__STRUCT_HPP_
