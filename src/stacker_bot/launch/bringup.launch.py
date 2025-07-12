from launch import LaunchDescription
from launch.actions import ExecuteProcess, SetEnvironmentVariable, TimerAction
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
from launch.substitutions import Command
from launch_ros.parameter_descriptions import ParameterValue
import os

def generate_launch_description():
    # Paths
    urdf_file = os.path.join(
        get_package_share_directory('franka_description'),
        'robots',
        'fr3',
        'fr3.urdf.xacro'
    )

    mesh_path = os.path.join(
        get_package_share_directory('franka_description'),
        'models'
    )

    controller_config = os.path.join(
        get_package_share_directory('stacker_bot'),
        'config',
        'franka_controllers.yaml'
    )

    sdf_file = os.path.join(
        get_package_share_directory('stacker_bot'),
        'worlds',
        'gz_world.world'
    )
    # Launch Gazebo with your world
    launch_gz_world = ExecuteProcess(
        cmd=['gz', 'sim', sdf_file],
        output='screen'
    )
    # Robot state publisher node
    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'robot_description': ParameterValue(
        Command(['xacro ', urdf_file, ' ros2_control:=true use_fake_hardware:=false gazebo:=true']),
        value_type=str)}],
        output='screen'
    )

    # Controller manager node
    controller_manager_node = Node(
        package='controller_manager',
        executable='ros2_control_node',
        parameters=[{'robot_description': ParameterValue(
        Command(['xacro ', urdf_file, ' ros2_control:=true use_fake_hardware:=false gazebo:=true']),
        value_type=str)}, controller_config],
        output='screen'
    )

    # Spawn the robot in Gazebo
    robot_to_gazebo = TimerAction(
        period=3.0,
        actions=[
            ExecuteProcess(
                cmd=[
                    'ros2', 'run', 'ros_gz_sim', 'create',
                    '-name', 'fr3',
                    '-topic', 'robot_description',
                    '-x', '0.0',
                    '-y', '-0.25',
                    '-z', '0.8',
                    '-R', '0.0',
                    '-P', '0.0',
                    '-Y', '1.55'
                ],
                output='screen'
            )
        ]
    )

    # Load joint_state_broadcaster after delay
    state_broadcaster_loader = TimerAction(
        period=5.0,
        actions=[
            ExecuteProcess(
                cmd=[
                    'ros2', 'control', 'load_controller',
                    '--set-state', 'active',
                    'joint_state_broadcaster'
                ],
                output='screen'
            )
        ]
    )

    # Load franka_arm_controller after delay
    franka_arm_controller = TimerAction(
        period=7.0,
        actions=[
            ExecuteProcess(
                cmd=[
                    'ros2', 'control', 'load_controller',
                    '--set-state', 'active',
                    'franka_arm_controller'
                ],
                output='screen'
            )
        ]
    )

    return LaunchDescription([
        SetEnvironmentVariable(
            name='GZ_SIM_RESOURCE_PATH',
            value=mesh_path
        ),
        launch_gz_world,
        robot_state_publisher_node,
        controller_manager_node,
        robot_to_gazebo,
        state_broadcaster_loader,
        franka_arm_controller
    ])
