from launch import LaunchDescription
from launch.actions import ExecuteProcess, SetEnvironmentVariable, TimerAction
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
from launch.substitutions import Command
from launch_ros.parameter_descriptions import ParameterValue
import os


def generate_launch_description():
    urdf_file = os.path.join(
        get_package_share_directory('franka_description'),
        'robots',
        'fr3',
        'fr3.urdf.xacro'
    )
    # Path to the mesh files
    mesh_path = os.path.join(
        get_package_share_directory('franka_description')
    ) 
    
    config_path = os.path.join(
        get_package_share_directory('stacker_bot'),
        'config',
        'framock nka_controllers.yaml'
    )
    # robot_state_publisher_node
    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'robot_description': ParameterValue(
        Command(['xacro ', urdf_file, ' ros2_control:=true use_fake_hardware:=false gazebo:=true']),
        value_type=str)}],
        output='screen'
    )
    
    # NOTE: For Gazebo simulation, we DON'T start ros2_control_node
    # The Gazebo plugin provides the controller manager functionality and the controllers are loaded via the plugin.

    # spawn the robot in Gazebo
    robot_to_gz = ExecuteProcess(
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
    # Load controllers
    load_joint_state_broadcaster = TimerAction(
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
    # Load arm position controller
    load_arm_position_controller = TimerAction(
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
        # Robot State Publisher
        robot_state_publisher_node,
        # NOTE: No controller_manager_node - Gazebo plugin provides this
        # spawn the robot in Gazebo
        robot_to_gz,
        # Load joint state broadcaster
        load_joint_state_broadcaster,
        # Load arm position controller
        load_arm_position_controller
    ])



