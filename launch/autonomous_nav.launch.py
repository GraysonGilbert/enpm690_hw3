
import os
import launch
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from webots_ros2_driver.webots_launcher import WebotsLauncher
from webots_ros2_driver.webots_controller import WebotsController
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration


def generate_launch_description():
    # Tunable Parameter
    threshold_arg = DeclareLaunchArgument(
        'sensor_threshold',
        default_value='0.1',
        description="Threshold distance in meters for robot to detect obstacle. [Max=0.15m, Min=0m]"
    )
    
    # Locate robot files
    webots_package_dir = get_package_share_directory('walker')
    robot_description_path = os.path.join(webots_package_dir, 'resource', 'my_robot.urdf')
    
    # Robot controller
    robot_driver_node = WebotsController(
        robot_name='walker_robot',
        parameters=[{'robot_description': robot_description_path},]
    )

    # Webots world
    webots = WebotsLauncher(
        world=os.path.join(webots_package_dir, 'worlds', 'my_world.wbt')
    )
    
    # Autonomy node
    autonomy_node = Node(
        package='enpm690_hw3',
        executable='autonomous_nav.py',
        name='autonomy_node',
        parameters=[{
            'threshold': LaunchConfiguration('sensor_threshold')}],
        output='screen'
    )


    return LaunchDescription([
        threshold_arg,
        webots,
        robot_driver_node,
        autonomy_node,
        launch.actions.RegisterEventHandler(
            event_handler=launch.event_handlers.OnProcessExit(
                target_action=webots,
                on_exit=[launch.actions.EmitEvent(event=launch.events.Shutdown())],
            )
            
        )
    ])