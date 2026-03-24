from glob import glob
import os
from setuptools import setup

package_name = 'py_robot_lab'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='user',
    maintainer_email='user@example.com',
    description='Practice package for Python x ROS 2',
    license='Apache License 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'fake_sensor_pub = py_robot_lab.fake_sensor_pub:main',
            'fake_sensor_sub = py_robot_lab.fake_sensor_sub:main',
            'add_two_ints_server = py_robot_lab.add_two_ints_server:main',
            'add_two_ints_client = py_robot_lab.add_two_ints_client:main',
            'turtle_circle = py_robot_lab.turtle_circle:main',
            'turtle_pose_sub = py_robot_lab.turtle_pose_sub:main',
            'fibonacci_action_server = py_robot_lab.fibonacci_action_server:main',
            'fibonacci_action_client = py_robot_lab.fibonacci_action_client:main',
            'param_monitor = py_robot_lab.param_monitor:main',
        ],
    },
)
