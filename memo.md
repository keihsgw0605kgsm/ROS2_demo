1. コンテナ起動
```
docker compose build
docker compose up -d
```

2. コンテナに入る
```
docker compose exec ros2_dev bash
```

3. (初回のみ)
3-1. Python package作成
```
mkdir -p src
cd src
ros2 pkg create \
--build-type ament_python \
py_robot_lab \
--dependencies rclpy std_msgs geometry_msgs example_interfaces turtlesim
```
workspace/src/py_robot_labができる

4. build
```
cd /root/ros2_ws
colcon build
source install/setup.bash
```

5. demo
```
ros2 run demo_nodes_cpp talker
```
別ターミナル
```
docker compose exec ros2_dev bash
ros2 run demo_nodes_py listener
```