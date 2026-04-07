import os
from ament_index_python.packages import get_package_share_path
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.substitutions import Command
from launch_ros.parameter_descriptions import ParameterValue

def generate_launch_description():
    # Rutas a tus archivos (Asegúrate que el URDF se llame Examenp1.urdf)
    pkg_path = get_package_share_path('robot_description')
    urdf_path = os.path.join(pkg_path, 'urdf', 'Examenp1.urdf')
    rviz_config_path = os.path.join(pkg_path, 'rviz', 'urdf.rviz')

    # Procesar el robot para que ROS lo entienda
    robot_description = ParameterValue(Command(['xacro ', urdf_path]), value_type=str)

    return LaunchDescription([
        # 1. Carga el modelo del robot
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            parameters=[{'robot_description': robot_description}]
        ),
        # 2. Abre RViz automáticamente
        Node(
            package='rviz2',
            executable='rviz2',
            arguments=['-d', str(rviz_config_path)]
        ),
        # 3. Lanza tu código de cinemática inversa
        Node(
            package='visual_pubsub',
            executable='inverse_kinematics',
            output='screen'
        )
    ])
