from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(
            package='turtlesim',
            executable='turtlesim_node',
            name='sim'
        ),
        Node(
            package='py_robot_lab',
            executable='turtle_circle',
            name='circle_controller'
        ),
        Node(
            package='py_robot_lab',
            executable='turtle_pose_sub',
            name='pose_monitor'
        ),
    ])
