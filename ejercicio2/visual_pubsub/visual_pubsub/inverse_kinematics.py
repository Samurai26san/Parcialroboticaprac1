import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from geometry_msgs.msg import Point, PointStamped
import numpy as np

from visual_pubsub_interfaces.srv import GetEndEffectorPose


class InverseKinematics(Node):

    def __init__(self):
        super().__init__('inverse_kinematics')

        self.joint_pub = self.create_publisher(JointState, 'joint_states', 10)

        self.ee_pose_pub = self.create_publisher(
            PointStamped, 'end_effector_pose', 10)

        self.target_sub = self.create_subscription(
            Point, 'target_position', self.target_callback, 10)

        self.ee_srv = self.create_service(
            GetEndEffectorPose,
            'get_end_effector_pose',
            self.handle_ee_pose)

        self.l1, self.l2, self.l3 = 3.0, 1.5, 1.5
        self.q = np.array([0.0, 0.0, 0.0, 0.0])

        self.target_pos = None
        self.timer_period = 0.02
        self.timer = self.create_timer(self.timer_period, self.update_joints)

        self.print_counter = 0
        self.print_every   = 50

        self.step_size = 0.05
        self.tolerance = 0.01
        self.damping   = 0.1

        self.get_logger().info(
            '=== IK node listo (4 joints) — esperando target ===\n'
            '    Servicio disponible: /get_end_effector_pose\n'
            '    Topic FK en tiempo real: /end_effector_pose')

    def forward_kinematics(self, q):
        q1, q2, q3 = q[0], q[1], q[2]
        dist_h = self.l2 * np.cos(q2) + self.l3 * np.cos(q2 + q3)
        x = dist_h * np.cos(q1)
        y = dist_h * np.sin(q1)
        z = self.l1 + self.l2 * np.sin(q2) + self.l3 * np.sin(q2 + q3)
        return np.array([x, y, z])

    def jacobian(self, q):
        q1, q2, q3 = q[0], q[1], q[2]
        c1,  s1  = np.cos(q1),      np.sin(q1)
        c2,  s2  = np.cos(q2),      np.sin(q2)
        c23, s23 = np.cos(q2 + q3), np.sin(q2 + q3)

        j11 = -(self.l2 * c2 + self.l3 * c23) * s1
        j12 = -(self.l2 * s2 + self.l3 * s23) * c1
        j13 = -self.l3 * s23 * c1
        j21 =  (self.l2 * c2 + self.l3 * c23) * c1
        j22 = -(self.l2 * s2 + self.l3 * s23) * s1
        j23 = -self.l3 * s23 * s1
        j31 = 0.0
        j32 = self.l2 * c2 + self.l3 * c23
        j33 = self.l3 * c23

        return np.array([[j11, j12, j13],
                         [j21, j22, j23],
                         [j31, j32, j33]])

    def target_callback(self, msg):
        self.target_pos = np.array([msg.x, msg.y, msg.z])
        self.get_logger().info(f'► Target: [{msg.x:.3f}, {msg.y:.3f}, {msg.z:.3f}]')
    def handle_ee_pose(self, request, response):
        """
        Calcula la FK para los ángulos recibidos en el request.
        Si q1=q2=q3=q4=0 se usan los ángulos actuales del nodo.
        """
        q_req = np.array([request.q1, request.q2, request.q3, request.q4])

        use_current = np.allclose(q_req, 0.0)
        q_eval = self.q.copy() if use_current else q_req

        pos = self.forward_kinematics(q_eval)

        error_norm = 0.0
        if self.target_pos is not None:
            error_norm = float(np.linalg.norm(self.target_pos - pos))

        response.x = float(pos[0])
        response.y = float(pos[1])
        response.z = float(pos[2])
        response.error_norm = error_norm

        src = 'estado actual del nodo' if use_current else \
              f'q=[{q_req[0]:.3f},{q_req[1]:.3f},{q_req[2]:.3f},{q_req[3]:.3f}]'
        response.status = (
            f'FK calculada para {src} → '
            f'p=({pos[0]:.4f}, {pos[1]:.4f}, {pos[2]:.4f})')

        self.get_logger().info(
            f'[SRV] {response.status}  |  ‖error‖={error_norm:.5f}')
        return response

    def _print_ik_state(self, current_pos, error, J, dq=None):
        sep = '─' * 52
        self.get_logger().info(f'\n{sep}')
        self.get_logger().info(
            f'  Joints  q = [{self.q[0]:7.4f}, {self.q[1]:7.4f}, '
            f'{self.q[2]:7.4f}, {self.q[3]:7.4f}] rad')
        self.get_logger().info(
            f'  FK pos  p = [{current_pos[0]:7.4f}, {current_pos[1]:7.4f}, '
            f'{current_pos[2]:7.4f}]')
        if self.target_pos is not None:
            self.get_logger().info(
                f'  Target  t = [{self.target_pos[0]:7.4f}, {self.target_pos[1]:7.4f}, '
                f'{self.target_pos[2]:7.4f}]')
        self.get_logger().info(
            f'  Error ‖e‖ = {np.linalg.norm(error):.6f}  '
            f'e = [{error[0]:7.4f}, {error[1]:7.4f}, {error[2]:7.4f}]')

        self.get_logger().info('  Jacobiana J (3×3):')
        labels = ['  Jx', '  Jy', '  Jz']
        for i, row in enumerate(J):
            self.get_logger().info(
                f'    {labels[i]} | {row[0]:8.5f}  {row[1]:8.5f}  {row[2]:8.5f} |')

        if dq is not None:
            self.get_logger().info(
                f'  Δq (IK)  = [{dq[0]:7.4f}, {dq[1]:7.4f}, {dq[2]:7.4f}]')
        self.get_logger().info(sep)

    def update_joints(self):
        current_pos = self.forward_kinematics(self.q)

        if self.target_pos is None:
            self._publish(current_pos)
            return

        error      = self.target_pos - current_pos
        error_norm = np.linalg.norm(error)

        J  = self.jacobian(self.q)
        dq = None

        if error_norm > self.tolerance:
            J_t   = J.T
            j_inv = np.linalg.inv(J_t @ J + self.damping * np.eye(3)) @ J_t
            dq    = j_inv @ error

            self.q[0:3] += np.clip(dq, -0.1, 0.1) * self.step_size
            self.q[1]    = np.clip(self.q[1], -1.5,  1.5)
            self.q[2]    = np.clip(self.q[2], -2.6,  2.6)
        else:
            self.get_logger().info('✔ Punto alcanzado')
            self.target_pos = None
            error = np.zeros(3)
            J     = self.jacobian(self.q)

        self.print_counter += 1
        if self.print_counter % self.print_every == 0:
            self._print_ik_state(current_pos, error, J, dq)

        self._publish(current_pos)

    def _publish(self, current_pos=None):
        js = JointState()
        js.header.stamp = self.get_clock().now().to_msg()
        js.name     = ['q1', 'q2', 'q3', 'q4']
        js.position = self.q.tolist()
        self.joint_pub.publish(js)

        if current_pos is None:
            current_pos = self.forward_kinematics(self.q)

        ee = PointStamped()
        ee.header.stamp    = js.header.stamp
        ee.header.frame_id = 'base_link'
        ee.point.x = float(current_pos[0])
        ee.point.y = float(current_pos[1])
        ee.point.z = float(current_pos[2])
        self.ee_pose_pub.publish(ee)


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