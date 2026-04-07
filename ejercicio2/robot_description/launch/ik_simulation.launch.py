
from ament_index_python.packages import get_package_share_path

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import Command, LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():

    urdf_tutorial_path = get_package_share_path('robot_description')
    default_model_path  = urdf_tutorial_path / 'urdf/tareaenclases.urdf'
    default_rviz_path   = urdf_tutorial_path / 'rviz/urdf.rviz'

    model_arg = DeclareLaunchArgument(
        name='model',
        default_value=str(default_model_path),
        description='Ruta absoluta al archivo URDF del robot')

    rviz_arg = DeclareLaunchArgument(
        name='rvizconfig',
        default_value=str(default_rviz_path),
        description='Ruta absoluta a la configuración de RViz2')

    robot_description = ParameterValue(
        Command(['xacro ', LaunchConfiguration('model')]),
        value_type=str)

    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{'robot_description': robot_description}]
    )

    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d', LaunchConfiguration('rvizconfig')],
    )

    inverse_kinematics_node = Node(
        package='visual_pubsub',
        executable='inv_joints',
        name='inverse_kinematics',
        output='screen',
    )

    return LaunchDescription([
        model_arg,
        rviz_arg,
        robot_state_publisher_node,
        rviz_node,
        inverse_kinematics_node,
    ])
