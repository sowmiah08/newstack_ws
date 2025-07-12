from launch import LaunchDescription
from launch.actions import ExecuteProcess
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    sdf_file = os.path.join(
        get_package_share_directory('stacker_bot'),
        'worlds',
        'gz_world.world'  # Replace with your actual SDF filename
    )
    return LaunchDescription([
        
        # SetEnvironmentVariable(name='GAZEBO_MODEL_PATH', value='~/workspaces/sow_ws/stack_env/src/stacker_bot/models'),

        ExecuteProcess(
            cmd=['gz', 'sim', sdf_file],
            output='screen'
        ),
    ])
 
