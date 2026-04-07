import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from geometry_msgs.msg import Point
import numpy as np

class InverseKinematics(Node):
    def __init__(self):
        super().__init__('inverse_kinematics')
        self.joint_pub = self.create_publisher(JointState, 'joint_states', 10)
        self.target_sub = self.create_subscription(Point, 'target_position', self.target_callback, 10)
        
        # Medidas URDF
        self.l1, self.l2, self.l3 = 3.0, 1.5, 1.5
        self.q = np.array([0.0, 0.0, 0.0]) 
        self.target_pos = np.array([1.5, 0.5, 3.5]) 

        # Control de frecuencia
        self.timer_period = 0.02 # 50Hz para suavidad
        self.timer = self.create_timer(self.timer_period, self.update_joints)
        
        # Contador para imprimir cada 1 segundo (50 ciclos * 0.02s = 1s)
        self.print_counter = 0
        
        self.step_size = 0.05
        self.tolerance = 0.01
        self.damping = 0.1

    def forward_kinematics(self, q):
        q1, q2, q3 = q
        dist_h = self.l2 * np.cos(q2) + self.l3 * np.cos(q2 + q3)
        x = dist_h * np.cos(q1)
        y = dist_h * np.sin(q1)
        z = self.l1 + self.l2 * np.sin(q2) + self.l3 * np.sin(q2 + q3)
        return np.array([x, y, z])

    def jacobian(self, q):
        q1, q2, q3 = q
        c1, s1 = np.cos(q1), np.sin(q1)
        c2, s2 = np.cos(q2), np.sin(q2)
        c23, s23 = np.cos(q2+q3), np.sin(q2+q3)

        j11 = -(self.l2 * c2 + self.l3 * c23) * s1
        j12 = -(self.l2 * s2 + self.l3 * s23) * c1
        j13 = -self.l3 * s23 * c1
        j21 = (self.l2 * c2 + self.l3 * c23) * c1
        j22 = -(self.l2 * s2 + self.l3 * s23) * s1
        j23 = -self.l3 * s23 * s1
        j31 = 0.0
        j32 = self.l2 * c2 + self.l3 * c23
        j33 = self.l3 * c23
        return np.array([[j11, j12, j13], [j21, j22, j23], [j31, j32, j33]])

    def target_callback(self, msg):
        self.target_pos = np.array([msg.x, msg.y, msg.z])

    def update_joints(self):
        current_pos = self.forward_kinematics(self.q)
        error = self.target_pos - current_pos
        J = self.jacobian(self.q)

        # --- LÓGICA DE IMPRESIÓN (Cada 1 segundo) ---
        self.print_counter += 1
        if self.print_counter >= 50:
            self.get_logger().info(f'\n--- MATRIZ JACOBIANA ---\n{J}\n------------------------')
            self.print_counter = 0

        if np.linalg.norm(error) > self.tolerance:
            J_t = J.T
            j_inv = np.linalg.inv(J_t @ J + self.damping * np.eye(3)) @ J_t
            dq = j_inv @ error
            
            dq_limited = np.clip(dq, -0.1, 0.1) 
            self.q += dq_limited * self.step_size

            # Límites de seguridad
            self.q[1] = np.clip(self.q[1], -1.5, 1.5)
            self.q[2] = np.clip(self.q[2], -2.6, 2.6)

        msg = JointState()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.name = ['q1', 'q2', 'q3']
        msg.position = self.q.tolist()
        self.joint_pub.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = InverseKinematics()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()