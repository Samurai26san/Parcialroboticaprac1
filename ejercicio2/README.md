# 🤖 Simulación de Cinemática Inversa con ROS 2 Jazzy + RViz2

Workspace de ROS 2 que implementa **cinemática inversa (IK)** para un brazo robótico de 4 articulaciones usando el método de la **pseudo-inversa Jacobiana amortiguada**. Incluye:

- Publicación en tiempo real de la posición del efector final.
- Servicio ROS 2 para calcular la **cinemática directa (FK)** a demanda.
- Visualización completa en **RViz2**.

---

## 📦 Paquetes del workspace

| Paquete | Descripción |
|---|---|
| `robot_description` | URDF del robot y archivos de configuración RViz2 |
| `visual_pubsub` | Nodo IK, publicador de joints y suscriptor |
| `visual_pubsub_interfaces` | Definición del servicio personalizado `GetEndEffectorPose` |

---

## ⚙️ Requisitos previos

- ROS 2 **Jazzy** instalado (`/opt/ros/jazzy`)
- Paquetes de ROS 2: `robot_state_publisher`, `rviz2`, `xacro`, `joint_state_publisher_gui`
- Python 3 con `numpy`

---

## 🔨 Compilar el workspace

Desde la **raíz del workspace** (donde está la carpeta `src` o los paquetes directamente):

```bash
# Ir a la raíz del workspace
cd ~/Roboticaclase/simulacion

# Cargar el entorno base de ROS 2
source /opt/ros/jazzy/setup.bash

# Compilar solo los paquetes relevantes
colcon build --packages-select visual_pubsub_interfaces visual_pubsub robot_description

# Cargar el entorno del workspace compilado
source install/setup.bash
```

> **Nota:** Cada vez que abras una nueva terminal debes ejecutar:
> ```bash
> source /opt/ros/jazzy/setup.bash
> source ~/Roboticaclase/simulacion/install/setup.bash
> ```

---

## 🚀 Lanzar la simulación completa

Este comando inicia el **robot_state_publisher**, **RViz2** y el **nodo de cinemática inversa** (que también expone el servicio FK):

```bash
ros2 launch robot_description ik_simulation.launch.py
```

Parámetros opcionales:

```bash
# Usar un URDF diferente
ros2 launch robot_description ik_simulation.launch.py model:=/ruta/al/robot.urdf

# Usar una configuración de RViz2 diferente
ros2 launch robot_description ik_simulation.launch.py rvizconfig:=/ruta/config.rviz
```

---

## 🦾 Mover el robot a un punto específico

Una vez lanzada la simulación, publica el punto cartesiano deseado `(x, y, z)` en el tópico `/target_position`.  
El nodo IK calculará los ángulos de articulación necesarios y moverá el robot iterativamente hasta alcanzar el objetivo.

```bash
ros2 topic pub --once /target_position geometry_msgs/msg/Point \
    "{x: 2.0, y: 1.0, z: 3.5}"
```

El robot se detendrá automáticamente cuando el error sea menor a `0.01` m.

### Ejemplos de puntos válidos

```bash
# Punto frontal medio
ros2 topic pub --once /target_position geometry_msgs/msg/Point "{x: 2.5, y: 0.0, z: 3.5}"

# Punto lateral izquierdo
ros2 topic pub --once /target_position geometry_msgs/msg/Point "{x: 1.0, y: 2.0, z: 4.0}"

# Punto bajo derecho
ros2 topic pub --once /target_position geometry_msgs/msg/Point "{x: 2.0, y: -1.5, z: 2.5}"
```

> ⚠️ Los límites del robot son: `l1 = 3.0`, `l2 = 1.5`, `l3 = 1.5`  
> El alcance máximo aproximado es `l2 + l3 = 3.0` en el plano horizontal.

---

## 📡 Consultar la posición del efector final

### Opción A — Tópico en tiempo real

El nodo publica continuamente la posición cartesiana del efector final:

```bash
ros2 topic echo /end_effector_pose
```

Salida esperada (`geometry_msgs/PointStamped`):

```
header:
  frame_id: base_link
point:
  x: 2.3451
  y: 0.0000
  z: 3.6712
```

Este tópico se puede visualizar en **RViz2** agregando un display de tipo `PointStamped`.

---

### Opción B — Servicio bajo demanda (`/get_end_effector_pose`)

Calcula la **cinemática directa** para cualquier configuración de articulaciones, sin necesidad de que el robot se mueva.

**Sintaxis general:**

```bash
ros2 service call /get_end_effector_pose \
    visual_pubsub_interfaces/srv/GetEndEffectorPose \
    "{q1: <valor>, q2: <valor>, q3: <valor>, q4: <valor>}"
```

**Ejemplos:**

```bash
# FK para ángulos específicos (en radianes)
ros2 service call /get_end_effector_pose \
    visual_pubsub_interfaces/srv/GetEndEffectorPose \
    "{q1: 0.0, q2: 0.5, q3: -0.5, q4: 0.0}"

# Consultar la posición actual del robot (todos los ángulos en 0.0)
ros2 service call /get_end_effector_pose \
    visual_pubsub_interfaces/srv/GetEndEffectorPose \
    "{q1: 0.0, q2: 0.0, q3: 0.0, q4: 0.0}"
```

**Respuesta del servicio:**

```
response:
  x: 2.1213
  y: 0.0000
  z: 4.1500
  error_norm: 0.03241    # distancia al último target (0.0 si no hay target activo)
  status: "FK calculada para q=[0.000,0.500,-0.500,0.000] → p=(2.1213, 0.0000, 4.1500)"
```

---

## 🗺️ Tópicos y servicios disponibles

| Nombre | Tipo | Dirección | Descripción |
|---|---|---|---|
| `/joint_states` | `sensor_msgs/JointState` | Publicado | Ángulos actuales de las 4 articulaciones |
| `/end_effector_pose` | `geometry_msgs/PointStamped` | Publicado | Posición FK del efector final en tiempo real |
| `/target_position` | `geometry_msgs/Point` | Suscrito | Punto cartesiano objetivo para la IK |
| `/get_end_effector_pose` | `GetEndEffectorPose` (srv) | Servicio | Calcula FK para ángulos dados a demanda |

---

## 🔍 Comandos de diagnóstico útiles

```bash
# Ver todos los tópicos activos
ros2 topic list

# Ver todos los servicios activos
ros2 service list

# Monitorear los ángulos de articulación
ros2 topic echo /joint_states

# Ver la frecuencia de publicación del efector final
ros2 topic hz /end_effector_pose

# Información del tipo del servicio
ros2 service type /get_end_effector_pose
```

---

## 📁 Estructura del workspace

```
simulacion/
├── ros2_tutorials/
│   ├── robot_description/
│   │   ├── launch/
│   │   │   ├── ik_simulation.launch.py   ← Launch principal
│   │   │   └── view_robot.launch.py
│   │   ├── urdf/
│   │   │   └── tareaenclases.urdf
│   │   └── rviz/
│   │       └── urdf.rviz
│   ├── visual_pubsub/
│   │   └── visual_pubsub/
│   │       ├── inverse_kinematics.py     ← Nodo IK + servidor FK
│   │       ├── pub_joints.py
│   │       └── sub_joints.py
│   └── visual_pubsub_interfaces/
│       └── srv/
│           └── GetEndEffectorPose.srv    ← Definición del servicio
└── README.md
```

---

## 📐 Modelo cinemático

El robot tiene **4 articulaciones** (`q1`, `q2`, `q3`, `q4`) con los siguientes parámetros:

| Parámetro | Valor | Descripción |
|---|---|---|
| `l1` | 3.0 m | Longitud del eslabón 1 (columna vertical) |
| `l2` | 1.5 m | Longitud del eslabón 2 |
| `l3` | 1.5 m | Longitud del eslabón 3 |
| `q1` | libre | Rotación en Z (yaw) |
| `q2` | [-1.5, 1.5] rad | Elevación del primer brazo |
| `q3` | [-2.6, 2.6] rad | Ángulo del segundo brazo |

**Cinemática directa:**

```
x = (l2·cos(q2) + l3·cos(q2+q3)) · cos(q1)
y = (l2·cos(q2) + l3·cos(q2+q3)) · sin(q1)
z = l1 + l2·sin(q2) + l3·sin(q2+q3)
```