from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    ld= LaunchDescription()
    simple_node= Node(
        package='stacker_bot',
        executable='simple_node',
        output='screen',
    )
    ld.add_action(simple_node)
    return ld
