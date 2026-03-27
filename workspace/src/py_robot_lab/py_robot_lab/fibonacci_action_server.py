import time

import rclpy
from example_interfaces.action import Fibonacci
from rclpy.action import ActionServer
from rclpy.node import Node


class FibonacciActionServer(Node):
    def __init__(self):
        super().__init__('fibonacci_action_server')
        self._action_server = ActionServer(
            self,
            Fibonacci,
            'fibonacci',
            execute_callback=self.execute_callback,
        )
        self.get_logger().info('Action server ready: /fibonacci')

    def execute_callback(self, goal_handle):
        order = goal_handle.request.order
        self.get_logger().info(f'Received goal order={order}')

        feedback_msg = Fibonacci.Feedback()
        feedback_msg.sequence = [0, 1]

        for i in range(2, order):
            if goal_handle.is_cancel_requested:
                goal_handle.canceled()
                self.get_logger().info('Goal canceled')
                result = Fibonacci.Result()
                result.sequence = feedback_msg.sequence
                return result

            feedback_msg.sequence.append(
                feedback_msg.sequence[i - 1] + feedback_msg.sequence[i - 2]
            )
            goal_handle.publish_feedback(feedback_msg)
            time.sleep(0.5)

        goal_handle.succeed()
        result = Fibonacci.Result()
        result.sequence = feedback_msg.sequence[:order] if order > 0 else []
        self.get_logger().info(f'Goal succeeded: {result.sequence}')
        return result


def main(args=None):
    rclpy.init(args=args)
    node = FibonacciActionServer()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
