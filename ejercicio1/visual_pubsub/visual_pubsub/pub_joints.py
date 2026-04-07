import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
import math
import time

class JointStatePublisher(Node):

    def __init__(self):
        super().__init__('joint_state_publisher')
        self.publisher_ = self.create_publisher(JointState, 'joint_states', 10)
        # Publicamos cada 0.05s (20Hz) para que el movimiento sea fluido en RViz
        self.timer = self.create_timer(0.05, self.publish_joint_states)
        self.start_time = time.time()

        # Parámetros constantes de tu tabla DH
        self.d1 = 1.0   # Altura de la base
        self.a2 = 0.5   # Longitud del brazo
        self.a3 = 0.3   # Longitud del antebrazo

    def publish_joint_states(self):
        # Calculamos el tiempo transcurrido para la función senoidal
        t = time.time() - self.start_time

        msg = JointState()
        msg.header.stamp = self.get_clock().now().to_msg()
        
        # Usamos los nombres de tus articulaciones: q1, q2, q3
        msg.name = ['q1', 'q2', 'q3']

        # --- MOVIMIENTO SUAVE (Ida y vuelta) ---
        # Definimos los ángulos como funciones del tiempo (ondas senoidales)
        # Amplitud * sin(Frecuencia * tiempo)
        q1_val = 1.2 * math.sin(0.5 * t)  # Oscilación de la cintura
        q2_val = 0.6 * math.sin(0.8 * t)  # Oscilación del hombro
        q3_val = 0.4 * math.sin(1.2 * t)  # Oscilación del codo

        msg.position = [q1_val, q2_val, q3_val]

        # --- CINEMÁTICA DIRECTA ---
        # Aplicamos las ecuaciones obtenidas de la Matriz T (A1*A2*A3) [cite: 4, 80]
        # Posición del efector final con respecto al sistema fijo [cite: 6, 7]
        px = math.cos(q1_val) * (self.a2 * math.cos(q2_val) + self.a3 * math.cos(q2_val + q3_val))
        py = math.sin(q1_val) * (self.a2 * math.cos(q2_val) + self.a3 * math.cos(q2_val + q3_val))
        pz = self.d1 - self.a2 * math.sin(q2_val) - self.a3 * math.sin(q2_val + q3_val)

        # Publicar los datos
        self.publisher_.publish(msg)

        # Log para visualizar el movimiento suave en la terminal
        self.get_logger().info(
            f'Joints: [{q1_val:.2f}, {q2_val:.2f}, {q3_val:.2f}] | Posición XYZ: [{px:.2f}, {py:.2f}, {pz:.2f}]'
        )

def main(args=None):
    rclpy.init(args=args)
    node = JointStatePublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()