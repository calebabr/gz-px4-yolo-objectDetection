// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from image_processing_msgs:msg/ProminentObjectArray.idl
// generated code does not contain a copyright notice

#ifndef IMAGE_PROCESSING_MSGS__MSG__DETAIL__PROMINENT_OBJECT_ARRAY__BUILDER_HPP_
#define IMAGE_PROCESSING_MSGS__MSG__DETAIL__PROMINENT_OBJECT_ARRAY__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "image_processing_msgs/msg/detail/prominent_object_array__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace image_processing_msgs
{

namespace msg
{

namespace builder
{

class Init_ProminentObjectArray_objects
{
public:
  Init_ProminentObjectArray_objects()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::image_processing_msgs::msg::ProminentObjectArray objects(::image_processing_msgs::msg::ProminentObjectArray::_objects_type arg)
  {
    msg_.objects = std::move(arg);
    return std::move(msg_);
  }

private:
  ::image_processing_msgs::msg::ProminentObjectArray msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::image_processing_msgs::msg::ProminentObjectArray>()
{
  return image_processing_msgs::msg::builder::Init_ProminentObjectArray_objects();
}

}  // namespace image_processing_msgs

#endif  // IMAGE_PROCESSING_MSGS__MSG__DETAIL__PROMINENT_OBJECT_ARRAY__BUILDER_HPP_
