
Sistema de publicadores y suscriptores en ROS2 con 5 nodos.

## Requisitos
- ROS2 Jazzy
- Python 3.12

## Instalación

### 1. Clonar el repositorio
```bash
git clone <url-de-tu-repo>
cd examenp1
```

### 2. Compilar el workspace
```bash
colcon build
source install/setup.bash
```

---

## Ejecutar con Launch (todos los nodos a la vez)
```bash
ros2 launch nodo1 launchejecutable.py
```

---

## Ejecutar cada nodo por separado

Abre una terminal diferente para cada nodo y en cada una ejecuta primero:
```bash
source install/setup.bash
```

**Terminal 1 - Nodo 1 (publicador):**
```bash
ros2 run nodo1 nodo1
```

**Terminal 2 - Nodo 2 (publicador):**
```bash
ros2 run nodo2 nodo2
```

**Terminal 3 - Nodo 3 (publicador):**
```bash
ros2 run nodo3 nodo3
```

**Terminal 4 - Nodo 4 (suscriptor/promedio):**
```bash
ros2 run nodo4 nodo4
```

**Terminal 5 - Nodo 5 (receptor del promedio):**
```bash
ros2 run nodo5 nodo5
```

---

## Visualizar el sistema

Ver nodos activos:
```bash
ros2 node list
```

Ver tópicos activos:
```bash
ros2 topic list
```

Ver grafo de nodos:
```bash
rqt_graph
```

---

## Arquitectura
