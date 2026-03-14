import math

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32


class FakeSensorPublisher(Node):
    def __init__(self):
        super().__init__('fake_sensor_publisher')
        self.publisher_ = self.create_publisher(Float32, 'fake_temperature', 10)
        self.timer = self.create_timer(0.5, self.timer_callback)
        self.t = 0.0

    def timer_callback(self):
        msg = Float32()
        msg.data = 25.0 + 5.0 * math.sin(self.t)
        self.publisher_.publish(msg)
        self.get_logger().info(f'Publish: {msg.data:.2f}')
        self.t += 0.2


def main(args=None):
    rclpy.init(args=args)
    node = FakeSensorPublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
