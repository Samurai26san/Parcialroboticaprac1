import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState

class JointStatePublisher(Node):

    def __init__(self):
        super().__init__('joint_state_publisher')
        self.publisher_ = self.create_publisher(JointState, 'joint_states', 10)
        
        self.timer = self.create_timer(0.5, self.publish_initial_state)
        self.get_logger().info('Nodo iniciado: Enviando solo posición inicial...')

    def publish_initial_state(self):
        msg = JointState()
        msg.header.stamp = self.get_clock().now().to_msg()
        
        msg.name = ['q1', 'q2', 'q3', 'q4']
        
        msg.position = [0.0, 0.0, 0.0, 0.0] 

        self.publisher_.publish(msg)
        self.get_logger().info(f'Posición inicial enviada: {msg.position}')
        
        self.timer.cancel()
        self.get_logger().info('Timer cancelado. El robot queda libre para otros nodos.')

def main(args=None):
    rclpy.init(args=args)
    node = JointStatePublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()