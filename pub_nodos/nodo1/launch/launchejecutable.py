from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='nodo1',
            executable='nodo1',
            name='nodo1'
        ),
        Node(
            package='nodo2',
            executable='nodo2',
            name='nodo2'
        ),
        Node(
            package='nodo3',
            executable='nodo3',
            name='nodo3'
        ),
        Node(
            package='nodo4',
            executable='nodo4',
            name='nodo4'
        ),
        Node(
            package='nodo5',
            executable='nodo5',
            name='nodo5'
        ),
    ])