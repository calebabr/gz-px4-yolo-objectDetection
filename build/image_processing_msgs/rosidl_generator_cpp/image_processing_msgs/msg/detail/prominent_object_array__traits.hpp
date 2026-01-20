// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from image_processing_msgs:msg/ProminentObjectArray.idl
// generated code does not contain a copyright notice

#ifndef IMAGE_PROCESSING_MSGS__MSG__DETAIL__PROMINENT_OBJECT_ARRAY__TRAITS_HPP_
#define IMAGE_PROCESSING_MSGS__MSG__DETAIL__PROMINENT_OBJECT_ARRAY__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "image_processing_msgs/msg/detail/prominent_object_array__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'objects'
#include "image_processing_msgs/msg/detail/prominent_object__traits.hpp"

namespace image_processing_msgs
{

namespace msg
{

inline void to_flow_style_yaml(
  const ProminentObjectArray & msg,
  std::ostream & out)
{
  out << "{";
  // member: objects
  {
    if (msg.objects.size() == 0) {
      out << "objects: []";
    } else {
      out << "objects: [";
      size_t pending_items = msg.objects.size();
      for (auto item : msg.objects) {
        to_flow_style_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const ProminentObjectArray & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: objects
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.objects.size() == 0) {
      out << "objects: []\n";
    } else {
      out << "objects:\n";
      for (auto item : msg.objects) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "-\n";
        to_block_style_yaml(item, out, indentation + 2);
      }
    }
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const ProminentObjectArray & msg, bool use_flow_style = false)
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
  const image_processing_msgs::msg::ProminentObjectArray & msg,
  std::ostream & out, size_t indentation = 0)
{
  image_processing_msgs::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use image_processing_msgs::msg::to_yaml() instead")]]
inline std::string to_yaml(const image_processing_msgs::msg::ProminentObjectArray & msg)
{
  return image_processing_msgs::msg::to_yaml(msg);
}

template<>
inline const char * data_type<image_processing_msgs::msg::ProminentObjectArray>()
{
  return "image_processing_msgs::msg::ProminentObjectArray";
}

template<>
inline const char * name<image_processing_msgs::msg::ProminentObjectArray>()
{
  return "image_processing_msgs/msg/ProminentObjectArray";
}

template<>
struct has_fixed_size<image_processing_msgs::msg::ProminentObjectArray>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<image_processing_msgs::msg::ProminentObjectArray>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<image_processing_msgs::msg::ProminentObjectArray>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // IMAGE_PROCESSING_MSGS__MSG__DETAIL__PROMINENT_OBJECT_ARRAY__TRAITS_HPP_
