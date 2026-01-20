// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from image_processing_msgs:msg/Detection.idl
// generated code does not contain a copyright notice

#ifndef IMAGE_PROCESSING_MSGS__MSG__DETAIL__DETECTION__BUILDER_HPP_
#define IMAGE_PROCESSING_MSGS__MSG__DETAIL__DETECTION__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "image_processing_msgs/msg/detail/detection__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace image_processing_msgs
{

namespace msg
{

namespace builder
{

class Init_Detection_pixel_area
{
public:
  explicit Init_Detection_pixel_area(::image_processing_msgs::msg::Detection & msg)
  : msg_(msg)
  {}
  ::image_processing_msgs::msg::Detection pixel_area(::image_processing_msgs::msg::Detection::_pixel_area_type arg)
  {
    msg_.pixel_area = std::move(arg);
    return std::move(msg_);
  }

private:
  ::image_processing_msgs::msg::Detection msg_;
};

class Init_Detection_height
{
public:
  explicit Init_Detection_height(::image_processing_msgs::msg::Detection & msg)
  : msg_(msg)
  {}
  Init_Detection_pixel_area height(::image_processing_msgs::msg::Detection::_height_type arg)
  {
    msg_.height = std::move(arg);
    return Init_Detection_pixel_area(msg_);
  }

private:
  ::image_processing_msgs::msg::Detection msg_;
};

class Init_Detection_width
{
public:
  explicit Init_Detection_width(::image_processing_msgs::msg::Detection & msg)
  : msg_(msg)
  {}
  Init_Detection_height width(::image_processing_msgs::msg::Detection::_width_type arg)
  {
    msg_.width = std::move(arg);
    return Init_Detection_height(msg_);
  }

private:
  ::image_processing_msgs::msg::Detection msg_;
};

class Init_Detection_y_center
{
public:
  explicit Init_Detection_y_center(::image_processing_msgs::msg::Detection & msg)
  : msg_(msg)
  {}
  Init_Detection_width y_center(::image_processing_msgs::msg::Detection::_y_center_type arg)
  {
    msg_.y_center = std::move(arg);
    return Init_Detection_width(msg_);
  }

private:
  ::image_processing_msgs::msg::Detection msg_;
};

class Init_Detection_x_center
{
public:
  explicit Init_Detection_x_center(::image_processing_msgs::msg::Detection & msg)
  : msg_(msg)
  {}
  Init_Detection_y_center x_center(::image_processing_msgs::msg::Detection::_x_center_type arg)
  {
    msg_.x_center = std::move(arg);
    return Init_Detection_y_center(msg_);
  }

private:
  ::image_processing_msgs::msg::Detection msg_;
};

class Init_Detection_y_max
{
public:
  explicit Init_Detection_y_max(::image_processing_msgs::msg::Detection & msg)
  : msg_(msg)
  {}
  Init_Detection_x_center y_max(::image_processing_msgs::msg::Detection::_y_max_type arg)
  {
    msg_.y_max = std::move(arg);
    return Init_Detection_x_center(msg_);
  }

private:
  ::image_processing_msgs::msg::Detection msg_;
};

class Init_Detection_x_max
{
public:
  explicit Init_Detection_x_max(::image_processing_msgs::msg::Detection & msg)
  : msg_(msg)
  {}
  Init_Detection_y_max x_max(::image_processing_msgs::msg::Detection::_x_max_type arg)
  {
    msg_.x_max = std::move(arg);
    return Init_Detection_y_max(msg_);
  }

private:
  ::image_processing_msgs::msg::Detection msg_;
};

class Init_Detection_y_min
{
public:
  explicit Init_Detection_y_min(::image_processing_msgs::msg::Detection & msg)
  : msg_(msg)
  {}
  Init_Detection_x_max y_min(::image_processing_msgs::msg::Detection::_y_min_type arg)
  {
    msg_.y_min = std::move(arg);
    return Init_Detection_x_max(msg_);
  }

private:
  ::image_processing_msgs::msg::Detection msg_;
};

class Init_Detection_x_min
{
public:
  explicit Init_Detection_x_min(::image_processing_msgs::msg::Detection & msg)
  : msg_(msg)
  {}
  Init_Detection_y_min x_min(::image_processing_msgs::msg::Detection::_x_min_type arg)
  {
    msg_.x_min = std::move(arg);
    return Init_Detection_y_min(msg_);
  }

private:
  ::image_processing_msgs::msg::Detection msg_;
};

class Init_Detection_confidence
{
public:
  explicit Init_Detection_confidence(::image_processing_msgs::msg::Detection & msg)
  : msg_(msg)
  {}
  Init_Detection_x_min confidence(::image_processing_msgs::msg::Detection::_confidence_type arg)
  {
    msg_.confidence = std::move(arg);
    return Init_Detection_x_min(msg_);
  }

private:
  ::image_processing_msgs::msg::Detection msg_;
};

class Init_Detection_class_name
{
public:
  Init_Detection_class_name()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Detection_confidence class_name(::image_processing_msgs::msg::Detection::_class_name_type arg)
  {
    msg_.class_name = std::move(arg);
    return Init_Detection_confidence(msg_);
  }

private:
  ::image_processing_msgs::msg::Detection msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::image_processing_msgs::msg::Detection>()
{
  return image_processing_msgs::msg::builder::Init_Detection_class_name();
}

}  // namespace image_processing_msgs

#endif  // IMAGE_PROCESSING_MSGS__MSG__DETAIL__DETECTION__BUILDER_HPP_
