// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from image_processing_msgs:msg/ProminentObject.idl
// generated code does not contain a copyright notice

#ifndef IMAGE_PROCESSING_MSGS__MSG__DETAIL__PROMINENT_OBJECT__STRUCT_HPP_
#define IMAGE_PROCESSING_MSGS__MSG__DETAIL__PROMINENT_OBJECT__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__image_processing_msgs__msg__ProminentObject __attribute__((deprecated))
#else
# define DEPRECATED__image_processing_msgs__msg__ProminentObject __declspec(deprecated)
#endif

namespace image_processing_msgs
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct ProminentObject_
{
  using Type = ProminentObject_<ContainerAllocator>;

  explicit ProminentObject_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->class_name = "";
      this->x_center = 0.0f;
      this->y_center = 0.0f;
      this->size_score = 0.0f;
    }
  }

  explicit ProminentObject_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : class_name(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->class_name = "";
      this->x_center = 0.0f;
      this->y_center = 0.0f;
      this->size_score = 0.0f;
    }
  }

  // field types and members
  using _class_name_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _class_name_type class_name;
  using _x_center_type =
    float;
  _x_center_type x_center;
  using _y_center_type =
    float;
  _y_center_type y_center;
  using _size_score_type =
    float;
  _size_score_type size_score;

  // setters for named parameter idiom
  Type & set__class_name(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->class_name = _arg;
    return *this;
  }
  Type & set__x_center(
    const float & _arg)
  {
    this->x_center = _arg;
    return *this;
  }
  Type & set__y_center(
    const float & _arg)
  {
    this->y_center = _arg;
    return *this;
  }
  Type & set__size_score(
    const float & _arg)
  {
    this->size_score = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    image_processing_msgs::msg::ProminentObject_<ContainerAllocator> *;
  using ConstRawPtr =
    const image_processing_msgs::msg::ProminentObject_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<image_processing_msgs::msg::ProminentObject_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<image_processing_msgs::msg::ProminentObject_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      image_processing_msgs::msg::ProminentObject_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<image_processing_msgs::msg::ProminentObject_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      image_processing_msgs::msg::ProminentObject_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<image_processing_msgs::msg::ProminentObject_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<image_processing_msgs::msg::ProminentObject_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<image_processing_msgs::msg::ProminentObject_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__image_processing_msgs__msg__ProminentObject
    std::shared_ptr<image_processing_msgs::msg::ProminentObject_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__image_processing_msgs__msg__ProminentObject
    std::shared_ptr<image_processing_msgs::msg::ProminentObject_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const ProminentObject_ & other) const
  {
    if (this->class_name != other.class_name) {
      return false;
    }
    if (this->x_center != other.x_center) {
      return false;
    }
    if (this->y_center != other.y_center) {
      return false;
    }
    if (this->size_score != other.size_score) {
      return false;
    }
    return true;
  }
  bool operator!=(const ProminentObject_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct ProminentObject_

// alias to use template instance with default allocator
using ProminentObject =
  image_processing_msgs::msg::ProminentObject_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace image_processing_msgs

#endif  // IMAGE_PROCESSING_MSGS__MSG__DETAIL__PROMINENT_OBJECT__STRUCT_HPP_
