import rclpy
from rcl_interfaces.msg import SetParametersResult
from rclpy.node import Node


class ParamMonitor(Node):
    def __init__(self):
        super().__init__('param_monitor')
        self.declare_parameter('message', 'hello from param_monitor')
        self.declare_parameter('log_period_sec', 1.0)

        self.add_on_set_parameters_callback(self._on_set_parameters)
        self.timer = self.create_timer(
            float(self.get_parameter('log_period_sec').value),
            self._timer_callback,
        )
        self.get_logger().info('Param monitor ready')

    def _on_set_parameters(self, params):
        new_period = None
        for param in params:
            if param.name == 'log_period_sec' and param.value <= 0:
                return SetParametersResult(
                    successful=False,
                    reason='log_period_sec must be > 0',
                )
            if param.name == 'log_period_sec':
                new_period = float(param.value)

        if new_period is not None:
            self.timer.cancel()
            self.timer = self.create_timer(new_period, self._timer_callback)
            self.get_logger().info(f'Updated timer period: {new_period:.1f}s')
        return SetParametersResult(successful=True)

    def _timer_callback(self):
        message = self.get_parameter('message').value
        period = float(self.get_parameter('log_period_sec').value)
        self.get_logger().info(f'message="{message}" period={period:.1f}s')


def main(args=None):
    rclpy.init(args=args)
    node = ParamMonitor()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
