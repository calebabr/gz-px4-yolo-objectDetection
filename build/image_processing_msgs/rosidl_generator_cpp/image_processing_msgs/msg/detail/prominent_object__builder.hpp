// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from image_processing_msgs:msg/ProminentObject.idl
// generated code does not contain a copyright notice

#ifndef IMAGE_PROCESSING_MSGS__MSG__DETAIL__PROMINENT_OBJECT__BUILDER_HPP_
#define IMAGE_PROCESSING_MSGS__MSG__DETAIL__PROMINENT_OBJECT__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "image_processing_msgs/msg/detail/prominent_object__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace image_processing_msgs
{

namespace msg
{

namespace builder
{

class Init_ProminentObject_size_score
{
public:
  explicit Init_ProminentObject_size_score(::image_processing_msgs::msg::ProminentObject & msg)
  : msg_(msg)
  {}
  ::image_processing_msgs::msg::ProminentObject size_score(::image_processing_msgs::msg::ProminentObject::_size_score_type arg)
  {
    msg_.size_score = std::move(arg);
    return std::move(msg_);
  }

private:
  ::image_processing_msgs::msg::ProminentObject msg_;
};

class Init_ProminentObject_y_center
{
public:
  explicit Init_ProminentObject_y_center(::image_processing_msgs::msg::ProminentObject & msg)
  : msg_(msg)
  {}
  Init_ProminentObject_size_score y_center(::image_processing_msgs::msg::ProminentObject::_y_center_type arg)
  {
    msg_.y_center = std::move(arg);
    return Init_ProminentObject_size_score(msg_);
  }

private:
  ::image_processing_msgs::msg::ProminentObject msg_;
};

class Init_ProminentObject_x_center
{
public:
  explicit Init_ProminentObject_x_center(::image_processing_msgs::msg::ProminentObject & msg)
  : msg_(msg)
  {}
  Init_ProminentObject_y_center x_center(::image_processing_msgs::msg::ProminentObject::_x_center_type arg)
  {
    msg_.x_center = std::move(arg);
    return Init_ProminentObject_y_center(msg_);
  }

private:
  ::image_processing_msgs::msg::ProminentObject msg_;
};

class Init_ProminentObject_class_name
{
public:
  Init_ProminentObject_class_name()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_ProminentObject_x_center class_name(::image_processing_msgs::msg::ProminentObject::_class_name_type arg)
  {
    msg_.class_name = std::move(arg);
    return Init_ProminentObject_x_center(msg_);
  }

private:
  ::image_processing_msgs::msg::ProminentObject msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::image_processing_msgs::msg::ProminentObject>()
{
  return image_processing_msgs::msg::builder::Init_ProminentObject_class_name();
}

}  // namespace image_processing_msgs

#endif  // IMAGE_PROCESSING_MSGS__MSG__DETAIL__PROMINENT_OBJECT__BUILDER_HPP_
