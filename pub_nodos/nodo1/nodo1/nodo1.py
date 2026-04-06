import rclpy
from rclpy.node import Node
import random
from std_msgs.msg import Float32MultiArray

class sensor1pub(Node):

    def __init__ (self):
        super().__init__('sensor_1pub')
        self.publisher_sensor1 = self.create_publisher(Float32MultiArray, 'sensor_1', 10)
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

    def timer_callback(self):
        msg_sensor1 = Float32MultiArray()
        senso = [random.uniform(0.00,10.0)]
        msg_sensor1.data = senso
        self.publisher_sensor1.publish(msg_sensor1)
        self.get_logger().info('El  nodo1 es: "%s"' % list(msg_sensor1.data))
        self.i += 1

def main(args=None):
    rclpy.init(args=args)

    sensor_1pub = sensor1pub()

    rclpy.spin(sensor_1pub)

    sensor_1pub.destroy_node()
    rclpy.shutdown()
if __name__ == '__main__':
    main()