Simulación de Brazo Robótico con IK (ROS 2 Jazzy + RViz2)

Este proyecto simula un brazo robótico de 4 articulaciones que puede moverse automáticamente hacia un punto en el espacio usando cinemática inversa (IK).

Incluye:
- Movimiento automático del robot a un punto (x, y, z)
- Visualización en RViz2
- Consulta de posición del efector final

Ubicación del proyecto:
~/Roboticaclase/simulacion

Compilar:
cd ~/Roboticaclase/simulacion
source /opt/ros/jazzy/setup.bash
colcon build --packages-select visual_pubsub_interfaces visual_pubsub robot_description
source install/setup.bash

Ejecutar la simulación:
ros2 launch robot_description ik_simulation.launch.py

Mover el robot:
ros2 topic pub --once /target_position geometry_msgs/msg/Point "{x: 2.0, y: 1.0, z: 3.5}"

Ejemplos:
ros2 topic pub --once /target_position geometry_msgs/msg/Point "{x: 2.5, y: 0.0, z: 3.5}"
ros2 topic pub --once /target_position geometry_msgs/msg/Point "{x: 1.0, y: 2.0, z: 4.0}"
ros2 topic pub --once /target_position geometry_msgs/msg/Point "{x: 2.0, y: -1.5, z: 2.5}"

Ver posición del efector final:
ros2 topic echo /end_effector_pose

Usar el servicio:
ros2 service call /get_end_effector_pose visual_pubsub_interfaces/srv/GetEndEffectorPose "{q1: 0.0, q2: 0.5, q3: -0.5, q4: 0.0}"

Comandos útiles:
ros2 topic list
ros2 service list
ros2 topic echo /joint_states
ros2 topic hz /end_effector_pose

Resumen rápido:
cd ~/Roboticaclase/simulacion
source /opt/ros/jazzy/setup.bash
colcon build
source install/setup.bash
ros2 launch robot_description ik_simulation.launch.py

ros2 topic pub --once /target_position geometry_msgs/msg/Point "{x: 2.0, y: 1.0, z: 3.5}"
