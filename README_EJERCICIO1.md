cd ~/Robotica/visual_ws/src

cat <<EOF > README.md
# Control de Brazo Robótico TRR - Cinemática Inversa

Este repositorio contiene la implementación de un algoritmo de cinemática inversa para un manipulador de tres grados de libertad (TRR).
El sistema utiliza el método del Jacobiano Amortiguado para garantizar la estabilidad en la vecindad de las singularidades.

## Estructura del repositorio
* **ejercicio1/robot_description**: Contiene el archivo URDF (Examenp1.urdf), la configuración de RViz y el script de lanzamiento maestro.
* **ejercicio1/visual_pubsub**: Contiene el nodo de control en Python encargado del cálculo diferencial y la publicación de estados de articulación.

## Requisitos de ejecución
1. Clonar el repositorio en la carpeta src de un workspace de ROS 2.
2. Compilar los paquetes:
   cd ~/tu_workspace
   colcon build --packages-select robot_description visual_pubsub
   source install/setup.bash

## Instrucciones de uso
Para iniciar la simulación completa (RViz + Nodo de control), ejecute el siguiente comando de lanzamiento:
ros2 launch robot_description robot_control.launch.py

Para enviar una coordenada de destino al efector final, utilice una terminal adicional con el siguiente comando:
ros2 topic pub /target_position geometry_msgs/msg/Point "{x: 1.5, y: 1.0, z: 4.5}" --once

## Detalles técnicos
* **Algoritmo**: Implementación de Damped Least Squares (DLS) para la inversión de la matriz Jacobiana, minimizando oscilaciones en extensiones máximas.
* **Salida de datos**: El nodo reporta la matriz Jacobiana calculada con una frecuencia de 1 Hz en la terminal de salida.
* **Restricciones de espacio**: El sistema está optimizado para objetivos con una coordenada Z > 3.0, correspondiente a la altura de la base fija (link1).
EOF

-------------------------------------------------------------------------------------------------------------------------------------
Bash
# 1. Agregar el archivo al índice de Git
git add README.md

# 2. Registrar el cambio
git commit -m "Add technical README documentation"

# 3. Enviar al repositorio remoto
git push origin main

---------------------------------------------------------------------------------------------------------------------------------------



