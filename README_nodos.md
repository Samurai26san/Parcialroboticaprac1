
Sistema de publicadores y suscriptores en ROS2 con 5 nodos.

## Requisitos
- ROS2 Jazzy
- Python 3.12

## Instalación

### 1. Clonar el repositorio
```bash
git clone [https://github.com/Samurai26san/Parcialroboticaprac1]
cd pub_nodos
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
ros2 run nodo1 nodo1 nodo1.py
```

**Terminal 2 - Nodo 2 (publicador):**
```bash
ros2 run nodo2 nodo2 nodo2.py
```

**Terminal 3 - Nodo 3 (publicador):**
```bash
ros2 run nodo3 nodo3 nodo3.py
```

**Terminal 4 - Nodo 4 (suscriptor/promedio):**
```bash
ros2 run nodo4 nodo4 nodo4.py
```

**Terminal 5 - Nodo 5 (receptor del promedio):**
```bash
ros2 run nodo5 nodo5 nodo5.py
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

- **nodo1, nodo2, nodo3**: Publican valores aleatorios (0.0 - 10.0)
- **nodo4**: Recibe los 3 valores, calcula sumatoria y promedio, publica a nodo5
- **nodo5**: Recibe el promedio final
