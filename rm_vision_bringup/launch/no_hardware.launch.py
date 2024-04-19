import os
import sys
from ament_index_python.packages import get_package_share_directory
sys.path.append(os.path.join(get_package_share_directory('rm_vision_bringup'), 'launch'))


def generate_launch_description():

    from common import launch_params, robot_state_publisher, node_params, armor_tracker_node, buff_tracker_node
    from launch_ros.actions import Node
    from launch import LaunchDescription

    armor_detector_node = Node(
        package='armor_detector',
        executable='armor_detector_node',
        emulate_tty=True,
        output='both',
        parameters=[node_params],
        arguments=['--ros-args', '--log-level',
                   'armor_detector:='+launch_params['armor_detector_log_level']],
    )

    buff_detector_node = Node(
        package='buff_detector',
        executable='buff_detector_node',
        emulate_tty=True,
        output='both',
        parameters=[node_params],
        arguments=['--ros-args', '--log-level',
                   'buff_detector:='+launch_params['buff_detector_log_level']],
    )

    return LaunchDescription([
        robot_state_publisher,
        armor_detector_node,
        buff_detector_node,
        armor_tracker_node,
        buff_tracker_node
    ])
