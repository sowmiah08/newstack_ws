cmake_minimum_required(VERSION 3.5.0)
project(gz_ros2_control_demos)

find_package(ros2_control_cmake REQUIRED)
set_compiler_options()
export_windows_symbols()

if(NOT WIN32)
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(ament_cmake REQUIRED)
find_package(control_msgs REQUIRED)
find_package(rclcpp REQUIRED)
find_package(rclcpp_action REQUIRED)
find_package(std_msgs REQUIRED)
find_package(geometry_msgs REQUIRED)

install(DIRECTORY
  launch
  config
  sdf
  urdf
  worlds
  DESTINATION share/${PROJECT_NAME}/
)

add_executable(example_position examples/example_position.cpp)
ament_target_dependencies(example_position
  rclcpp
  rclcpp_action
  control_msgs
)

# use the same example_position.cpp for example_velocity
add_executable(example_velocity examples/example_position.cpp)
ament_target_dependencies(example_velocity
  rclcpp
  rclcpp_action
  control_msgs
)

# use the same example_position.cpp for example_effort
add_executable(example_effort examples/example_position.cpp)
ament_target_dependencies(example_effort
  rclcpp
  rclcpp_action
  control_msgs
)

add_executable(example_diff_drive examples/example_diff_drive.cpp)
ament_target_dependencies(example_diff_drive
  rclcpp
  geometry_msgs
)

add_executable(example_tricycle_drive examples/example_tricycle_drive.cpp)
ament_target_dependencies(example_tricycle_drive
  rclcpp
  geometry_msgs
)

add_executable(example_ackermann_drive examples/example_ackermann_drive.cpp)
ament_target_dependencies(example_ackermann_drive
  rclcpp
  geometry_msgs
)

add_executable(example_gripper examples/example_gripper.cpp)
ament_target_dependencies(example_gripper
  rclcpp
  std_msgs
)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)

  ament_lint_auto_find_test_dependencies()
endif()

## Install
install(
  TARGETS
    example_position
    example_velocity
    example_effort
    example_diff_drive
    example_tricycle_drive
    example_ackermann_drive
    example_gripper
  DESTINATION
    lib/${PROJECT_NAME}
)

ament_package()
