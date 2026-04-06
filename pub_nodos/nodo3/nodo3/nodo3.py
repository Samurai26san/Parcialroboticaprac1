import rclpy
from rclpy.node import Node
import random
from std_msgs.msg import Float32MultiArray

class sensor1pub(Node):

    def __init__ (self):
        super().__init__('sensor_3pub')
        self.publisher_sensor3 = self.create_publisher(Float32MultiArray, 'sensor_3', 10)
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

    def timer_callback(self):
        msg_sensor3 = Float32MultiArray()
        senso = [random.uniform(0.00,10.00)]
        msg_sensor3.data = senso
        self.publisher_sensor3.publish(msg_sensor3)
        self.get_logger().info('El nodo3 es: "%s"' % list(msg_sensor3.data))
        self.i += 1

def main(args=None):
    rclpy.init(args=args)

    sensor_3pub = sensor1pub()

    rclpy.spin(sensor_3pub)

    sensor_3pub.destroy_node()
    rclpy.shutdown()
if __name__ == '__main__':
    main()