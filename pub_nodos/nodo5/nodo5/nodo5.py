import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32MultiArray

class sensor5sub(Node):

    def __init__(self):
        super().__init__('nodo_5')
        self.subscription = self.create_subscription(
            Float32MultiArray,
            'sensor_5',
            self.listener_callback,
            10)

    def listener_callback(self, msg):
        self.get_logger().info('Promedio recibido: "%s"' % list(msg.data))

def main(args=None):
    rclpy.init(args=args)
    nodo_5 = sensor5sub()
    rclpy.spin(nodo_5)
    nodo_5.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()