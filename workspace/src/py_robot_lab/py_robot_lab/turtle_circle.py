import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist


class TurtleCircle(Node):
    def __init__(self):
        super().__init__('turtle_circle')
        self.pub = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.timer = self.create_timer(0.1, self.callback)
        self._log_counter = 0

    def callback(self):
        msg = Twist()
        msg.linear.x = 2.0
        msg.angular.z = 1.0
        self.pub.publish(msg)
        self._log_counter += 1

        # 10Hz publishだとログが多すぎるため、1秒に1回だけ表示する。
        if self._log_counter % 10 == 0:
            self.get_logger().info(
                f'publishing /turtle1/cmd_vel linear.x={msg.linear.x:.1f}, angular.z={msg.angular.z:.1f}'
            )


def main(args=None):
    rclpy.init(args=args)
    node = TurtleCircle()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
