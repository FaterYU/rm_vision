import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command, LaunchConfiguration, PythonExpression

from launch_ros.actions import ComposableNodeContainer, Node
from launch_ros.descriptions import ComposableNode

camera_type = LaunchConfiguration('camera')
declare_camera_type_cmd = DeclareLaunchArgument(
    'camera',
    default_value='hik',
    description='Available camera types: hik, mv')

params_file = os.path.join(
    get_package_share_directory('rm_vision_bringup'), 'config', 'params.yaml')

robot_description = Command(['xacro ', os.path.join(
    get_package_share_directory('rm_gimbal_description'),
    'urdf', 'rm_gimbal.urdf.xacro')])


def camera_node(package, plugin):
    return ComposableNode(
        package=package,
        plugin=plugin,
        name='camera_node',
        parameters=[params_file],
        extra_arguments=[{'use_intra_process_comms': True}]
    )


def camera_detector_container(camera_node, condition):
    return ComposableNodeContainer(
        name='camera_detector_container',
        namespace='',
        package='rclcpp_components',
        executable='component_container',
        condition=condition,
        composable_node_descriptions=[
            camera_node,
            ComposableNode(
                package='armor_detector',
                plugin='rm_auto_aim::ArmorDetectorNode',
                name='armor_detector',
                parameters=[params_file],
                extra_arguments=[{'use_intra_process_comms': True}]
            )
        ],
        output='screen',
        emulate_tty=True,
        ros_arguments=['--log-level', 'armor_detector:=DEBUG'],
    )


hik_camera_node = camera_node('hik_camera', 'hik_camera::HikCameraNode')
hik_camera_detector_container = camera_detector_container(
    hik_camera_node, IfCondition(PythonExpression(["'", camera_type, "'=='hik'"])))

mv_camera_node = camera_node('mindvision_camera', 'mindvision_camera::MVCameraNode')
mv_camera_detector_container = camera_detector_container(
    mv_camera_node, IfCondition(PythonExpression(["'", camera_type, "'=='mv'"])))

tracker_node = Node(
    package='armor_tracker',
    executable='armor_tracker_node',
    output='screen',
    emulate_tty=True,
    parameters=[params_file],
    ros_arguments=['--log-level', 'armor_tracker:=DEBUG'],
)

robot_state_publisher = Node(
    package='robot_state_publisher',
    executable='robot_state_publisher',
    parameters=[{'robot_description': robot_description,
                 'publish_frequency': 1000.0}]
)

rm_serial_launch = IncludeLaunchDescription(
    PythonLaunchDescriptionSource(
        os.path.join(
            get_package_share_directory('rm_serial_driver'),
            'launch', 'serial_driver.launch.py')),
)


def generate_launch_description():
    return LaunchDescription([
        declare_camera_type_cmd,
        mv_camera_detector_container,
        hik_camera_detector_container,
        tracker_node,
        robot_state_publisher,
        rm_serial_launch,
    ])
