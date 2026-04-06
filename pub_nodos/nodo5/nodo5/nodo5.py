import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32MultiArray
from sensor_msgs_custom.msg import FilteredSensor

class sensor3sub(Node):

    def __init__(self):
        super().__init__('sensor_subscriber')
        self.data1 = None
        self.data2 = None
        self.data3 = None

        self.publisher_nodo5 = self.create_publisher(FilteredSensor, 'filtered_sensor', 10)

        self.subscription1 = self.create_subscription(
            Float32MultiArray, 'sensor_1', self.listener_callback_1, 10)
        self.subscription2 = self.create_subscription(
            Float32MultiArray, 'sensor_2', self.listener_callback_2, 10)
        self.subscription3 = self.create_subscription(
            Float32MultiArray, 'sensor_3', self.listener_callback_3, 10)

    def listener_callback_1(self, msg):
        self.get_logger().info('Nodo 1 recibido: "%s"' % list(msg.data))
        self.data1 = msg.data
        self.sumatoria_prom()

    def listener_callback_2(self, msg):
        self.get_logger().info('Nodo 2 recibido: "%s"' % list(msg.data))
        self.data2 = msg.data
        self.sumatoria_prom()

    def listener_callback_3(self, msg):
        self.get_logger().info('Nodo 3 recibido: "%s"' % list(msg.data))
        self.data3 = msg.data
        self.sumatoria_prom()

    def sumatoria_prom(self):
        if self.data1 is None or self.data2 is None or self.data3 is None:
            return

        sumatoria = sum(self.data1) + sum(self.data2) + sum(self.data3)
        promedio = sumatoria / 3
        self.get_logger().info('La sumatoria es: "%s"' % sumatoria)
        self.get_logger().info('El promedio es: "%s"' % promedio)

        msg_out = FilteredSensor()
        msg_out.sensor_value = promedio
        msg_out.name = 'promedio_sensores'
        self.publisher_nodo5.publish(msg_out)

def main(args=None):
    rclpy.init(args=args)
    sensor_3sub = sensor3sub()
    rclpy.spin(sensor_3sub)
    sensor_3sub.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()