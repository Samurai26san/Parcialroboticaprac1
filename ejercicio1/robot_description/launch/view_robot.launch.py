"""
    Author: carlos 
"""
from ament_index_python.packages import get_package_share_path
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import Command, LaunchConfiguration

def generate_launch_description():
    """
    launch method
    """
    urdf_tutorial_path = get_package_share_path('robot_description')
    # Asegúrate de que este nombre de archivo URDF sea el correcto
    default_model_path = urdf_tutorial_path / 'urdf/Examenp1.urdf'
    default_rviz_config_path = urdf_tutorial_path / 'rviz/urdf.rviz'

    # 1. Ponemos el GUI en 'false' por defecto
    gui_arg = DeclareLaunchArgument(
        name='gui',
        default_value='false', 
        choices=['true', 'false'],
        description='Flag to enable joint_state_publisher_gui')

    model_arg = DeclareLaunchArgument(
        name='model',
        default_value=str(default_model_path),
        description='Absolute path to robot urdf file')

    rviz_arg = DeclareLaunchArgument(
        name='rvizconfig',
        default_value=str(default_rviz_config_path),
        description='Absolute path to rviz config file')

    robot_description = ParameterValue(
        Command(['xacro ', LaunchConfiguration('model')]),
        value_type=str)

    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'robot_description': robot_description}]
    )

    # 2. Nodo estándar: lo dejamos SIN GUI para que no estorbe a tu PUB
    joint_state_publisher_node = Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        parameters=[{'use_gui': False}]
    )

    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d', LaunchConfiguration('rvizconfig')],
    )

    # 3. Retornamos la descripción SIN el nodo de la GUI
    return LaunchDescription([
        gui_arg, 
        model_arg, 
        rviz_arg, 
        joint_state_publisher_node,
        # HEMOS QUITADO EL joint_state_publisher_gui_node DE AQUÍ
        robot_state_publisher_node, 
        rviz_node
    ])