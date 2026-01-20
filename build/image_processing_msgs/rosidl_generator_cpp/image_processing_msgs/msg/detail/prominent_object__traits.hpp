// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from image_processing_msgs:msg/ProminentObject.idl
// generated code does not contain a copyright notice

#ifndef IMAGE_PROCESSING_MSGS__MSG__DETAIL__PROMINENT_OBJECT__TRAITS_HPP_
#define IMAGE_PROCESSING_MSGS__MSG__DETAIL__PROMINENT_OBJECT__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "image_processing_msgs/msg/detail/prominent_object__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace image_processing_msgs
{

namespace msg
{

inline void to_flow_style_yaml(
  const ProminentObject & msg,
  std::ostream & out)
{
  out << "{";
  // member: class_name
  {
    out << "class_name: ";
    rosidl_generator_traits::value_to_yaml(msg.class_name, out);
    out << ", ";
  }

  // member: x_center
  {
    out << "x_center: ";
    rosidl_generator_traits::value_to_yaml(msg.x_center, out);
    out << ", ";
  }

  // member: y_center
  {
    out << "y_center: ";
    rosidl_generator_traits::value_to_yaml(msg.y_center, out);
    out << ", ";
  }

  // member: size_score
  {
    out << "size_score: ";
    rosidl_generator_traits::value_to_yaml(msg.size_score, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const ProminentObject & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: class_name
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "class_name: ";
    rosidl_generator_traits::value_to_yaml(msg.class_name, out);
    out << "\n";
  }

  // member: x_center
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "x_center: ";
    rosidl_generator_traits::value_to_yaml(msg.x_center, out);
    out << "\n";
  }

  // member: y_center
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "y_center: ";
    rosidl_generator_traits::value_to_yaml(msg.y_center, out);
    out << "\n";
  }

  // member: size_score
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "size_score: ";
    rosidl_generator_traits::value_to_yaml(msg.size_score, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const ProminentObject & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace msg

}  // namespace image_processing_msgs

namespace rosidl_generator_traits
{

[[deprecated("use image_processing_msgs::msg::to_block_style_yaml() instead")]]
inline void to_yaml(
  const image_processing_msgs::msg::ProminentObject & msg,
  std::ostream & out, size_t indentation = 0)
{
  image_processing_msgs::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use image_processing_msgs::msg::to_yaml() instead")]]
inline std::string to_yaml(const image_processing_msgs::msg::ProminentObject & msg)
{
  return image_processing_msgs::msg::to_yaml(msg);
}

template<>
inline const char * data_type<image_processing_msgs::msg::ProminentObject>()
{
  return "image_processing_msgs::msg::ProminentObject";
}

template<>
inline const char * name<image_processing_msgs::msg::ProminentObject>()
{
  return "image_processing_msgs/msg/ProminentObject";
}

template<>
struct has_fixed_size<image_processing_msgs::msg::ProminentObject>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<image_processing_msgs::msg::ProminentObject>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<image_processing_msgs::msg::ProminentObject>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // IMAGE_PROCESSING_MSGS__MSG__DETAIL__PROMINENT_OBJECT__TRAITS_HPP_
