import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32


class FakeSensorSubscriber(Node):
    def __init__(self):
        super().__init__('fake_sensor_subscriber')
        self.subscription = self.create_subscription(
            Float32,
            'fake_temperature',
            self.listener_callback,
            10
        )

    def listener_callback(self, msg):
        self.get_logger().info(f'Receive: {msg.data:.2f}')


def main(args=None):
    rclpy.init(args=args)
    node = FakeSensorSubscriber()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
