import rclpy
from rclpy.node import Node
import random
from std_msgs.msg import Float32MultiArray

class sensor1pub(Node):

    def __init__ (self):
        super().__init__('sensor_2pub')
        self.publisher_sensor2 = self.create_publisher(Float32MultiArray, 'sensor_2', 10)
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

    def timer_callback(self):
        msg_sensor2 = Float32MultiArray()
        senso = [random.uniform(0.00,10.00)]
        msg_sensor2.data = senso
        self.publisher_sensor2.publish(msg_sensor2)
        self.get_logger().info('El nodo2 es "%s"' % list(msg_sensor2.data))
        self.i += 1

def main(args=None):
    rclpy.init(args=args)

    sensor_2pub = sensor1pub()

    rclpy.spin(sensor_2pub)

    sensor_2pub.destroy_node()
    rclpy.shutdown()
if __name__ == '__main__':
    main()