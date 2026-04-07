import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState

class JointStateSubscriber(Node):
    def __init__(self):
        super().__init__('joint_state_subscriber')
        self.subscription = self.create_subscription(
            JointState,
            'joint_states',
            self.listener_callback,
            10)

    def listener_callback(self, msg):
        self.get_logger().info('--- Lectura de Articulaciones ---')
        for name, pos in zip(msg.name, msg.position):
            # Mostramos el valor en radianes
            self.get_logger().info(f'Joint {name}: {pos:.3f} rad')

def main(args=None):
    rclpy.init(args=args)
    node = JointStateSubscriber()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()