// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from image_processing_msgs:msg/DetectionArray.idl
// generated code does not contain a copyright notice

#ifndef IMAGE_PROCESSING_MSGS__MSG__DETAIL__DETECTION_ARRAY__BUILDER_HPP_
#define IMAGE_PROCESSING_MSGS__MSG__DETAIL__DETECTION_ARRAY__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "image_processing_msgs/msg/detail/detection_array__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace image_processing_msgs
{

namespace msg
{

namespace builder
{

class Init_DetectionArray_detections
{
public:
  Init_DetectionArray_detections()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::image_processing_msgs::msg::DetectionArray detections(::image_processing_msgs::msg::DetectionArray::_detections_type arg)
  {
    msg_.detections = std::move(arg);
    return std::move(msg_);
  }

private:
  ::image_processing_msgs::msg::DetectionArray msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::image_processing_msgs::msg::DetectionArray>()
{
  return image_processing_msgs::msg::builder::Init_DetectionArray_detections();
}

}  // namespace image_processing_msgs

#endif  // IMAGE_PROCESSING_MSGS__MSG__DETAIL__DETECTION_ARRAY__BUILDER_HPP_
