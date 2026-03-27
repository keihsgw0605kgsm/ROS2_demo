import rclpy
from example_interfaces.action import Fibonacci
from rclpy.action import ActionClient
from rclpy.node import Node


class FibonacciActionClient(Node):
    def __init__(self):
        super().__init__('fibonacci_action_client')
        self._client = ActionClient(self, Fibonacci, 'fibonacci')

    def send_goal(self, order):
        self._client.wait_for_server()

        goal_msg = Fibonacci.Goal()
        goal_msg.order = order

        self.get_logger().info(f'Sending goal order={order}')
        send_goal_future = self._client.send_goal_async(
            goal_msg,
            feedback_callback=self.feedback_callback,
        )
        send_goal_future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info('Goal rejected')
            rclpy.shutdown()
            return

        self.get_logger().info('Goal accepted')
        result_future = goal_handle.get_result_async()
        result_future.add_done_callback(self.result_callback)

    def feedback_callback(self, feedback_msg):
        self.get_logger().info(f'Feedback: {feedback_msg.feedback.sequence}')

    def result_callback(self, future):
        result = future.result().result
        self.get_logger().info(f'Result: {result.sequence}')
        rclpy.shutdown()


def main(args=None):
    rclpy.init(args=args)
    node = FibonacciActionClient()

    order = 10
    cli_args = rclpy.utilities.remove_ros_args(args)
    if len(cli_args) > 1:
        try:
            order = int(cli_args[1])
        except ValueError:
            node.get_logger().warn('Invalid order. Use integer, fallback to 10.')

    node.send_goal(order)
    rclpy.spin(node)
    node.destroy_node()


if __name__ == '__main__':
    main()
