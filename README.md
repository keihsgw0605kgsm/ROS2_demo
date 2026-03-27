# ROS 2 Docker Starter (Humble + Python)

macOS 上で Docker を使い、ROS 2 Humble の基本通信。  
ログと CLI 出力だけでも学習・検証できる構成。

## What This Repository Solves

- **環境構築のハードルを下げる**: ローカルに ROS 2 を直接インストールせず、Docker で再現性のある開発環境を起動
- **ROS 2 通信の最短理解**: `topic` / `service` / `action` / `parameter` を最小ノードで体験
- **ロボット実務への接続**: 各章に「目的」「用途例」「成功条件」を明記し、現場での使い所を理解

## Features

- ROS 2 Humble (desktop) コンテナ
- Python パッケージ `py_robot_lab` 同梱
- 以下のサンプルノードを実装済み
  - Pub/Sub: `fake_sensor_pub`, `fake_sensor_sub`
  - Service: `add_two_ints_server`, `add_two_ints_client`
  - Turtle control: `turtle_circle`, `turtle_pose_sub`
  - Action: `fibonacci_action_server`, `fibonacci_action_client`
  - Parameter: `param_monitor`

## Directory Layout

```text
.
|-- Dockerfile
|-- docker-compose.yml
`-- workspace/
    `-- src/
        `-- py_robot_lab/
```

## Prerequisites

- macOS
- Docker Desktop
- Docker Compose v2 (`docker compose`)

## Quick Start

### 1) Build and Start Container

```bash
docker compose build
docker compose up -d
```

### 2) Enter Container

```bash
docker compose exec ros2_dev bash
source /opt/ros/humble/setup.bash
```

### 3) Build Workspace

```bash
cd /root/ros2_ws
colcon build --symlink-install
source install/setup.bash
```

### 4) Sanity Check

```bash
ros2 pkg executables py_robot_lab
```

## Learning Goal and Completion Criteria

このリポジトリの到達目標:

- 画面表示がなくても、**ログとトピック/サービス出力だけで「通信できた」を判定**できる
- `topic` / `service` / `action` / `parameter` の 4 種類を、最小ノードで 1 回ずつ成功させる
- 各章の「成功条件」を満たしたら完了

---

## 1. Topic (Pub/Sub): fake sensor

### 目的

Publisher が送信したデータを Subscriber が受信する、ROS 2 の非同期通信の基本を確認する。

### 用途例（ロボット）

- LiDAR / カメラ / IMU / 温度などのセンサ値を周期配信し、複数ノードで同時利用
- 自律走行で、認識ノード・地図ノード・記録ノードが同じセンサトピックを購読

### 実行

端末 1:
```bash
docker compose exec ros2_dev bash -lc "source /opt/ros/humble/setup.bash && cd /root/ros2_ws && source install/setup.bash && ros2 run py_robot_lab fake_sensor_pub"
```

端末 2:
```bash
docker compose exec ros2_dev bash -lc "source /opt/ros/humble/setup.bash && cd /root/ros2_ws && source install/setup.bash && ros2 run py_robot_lab fake_sensor_sub"
```

補助確認（任意）:
```bash
docker compose exec ros2_dev bash -lc "source /opt/ros/humble/setup.bash && cd /root/ros2_ws && source install/setup.bash && ros2 topic list"
docker compose exec ros2_dev bash -lc "source /opt/ros/humble/setup.bash && cd /root/ros2_ws && source install/setup.bash && ros2 topic echo /fake_temperature"
```

### 成功条件

- Subscriber 側で温度データを継続受信できる
- `/fake_temperature` が `ros2 topic list` に表示される

---

## 2. Service: AddTwoInts

### 目的

Client が Server に 1 回リクエストを送り、レスポンスを受け取る同期通信を確認する。

### 用途例（ロボット）

- センサ校正開始、地図保存、現在姿勢問い合わせなど「1 回だけ必要な処理」を実行
- `save_map` や `reset_odometry` のような「即時実行 + 結果返却」操作

### 実行

端末 1:
```bash
docker compose exec ros2_dev bash -lc "source /opt/ros/humble/setup.bash && cd /root/ros2_ws && source install/setup.bash && ros2 run py_robot_lab add_two_ints_server"
```

端末 2:
```bash
docker compose exec ros2_dev bash -lc "source /opt/ros/humble/setup.bash && cd /root/ros2_ws && source install/setup.bash && ros2 run py_robot_lab add_two_ints_client 10 32"
```

### 成功条件

- Client 側で計算結果が表示される
- Server 側でリクエスト受信ログを確認できる

---

## 3. Turtle Control (Topic): velocity command + pose monitor

### 目的

移動体へ速度指令を連続送信し、状態トピックで挙動を監視する流れを確認する。

### 用途例（ロボット）

- `/cmd_vel` で移動ロボットを制御し、`/odom` や自己位置推定を監視
- 速度指令ノードと位置モニタノードを分離し、機能ごとに保守しやすく運用

### 実行フェーズの前提

- 直前で未ビルドなら一度だけ実行:

```bash
docker compose exec ros2_dev bash -lc "source /opt/ros/humble/setup.bash && cd /root/ros2_ws && colcon build --symlink-install && source install/setup.bash"
```

### 実行（3 端末）

端末 1（シミュレータ）:
```bash
docker compose exec ros2_dev bash -lc "source /opt/ros/humble/setup.bash && export QT_QPA_PLATFORM=offscreen && ros2 run turtlesim turtlesim_node"
```

端末 2（制御）:
```bash
docker compose exec ros2_dev bash -lc "source /opt/ros/humble/setup.bash && cd /root/ros2_ws && source install/setup.bash && ros2 run py_robot_lab turtle_circle"
```

端末 3（監視）:
```bash
docker compose exec ros2_dev bash -lc "source /opt/ros/humble/setup.bash && cd /root/ros2_ws && source install/setup.bash && ros2 run py_robot_lab turtle_pose_sub"
```

補助確認（任意）:
```bash
docker compose exec ros2_dev bash -lc "source /opt/ros/humble/setup.bash && ros2 topic echo /turtle1/cmd_vel"
```

### 成功条件

- 監視端末で `x=..., y=..., theta=...` が時間とともに変化する
- 制御端末で `/turtle1/cmd_vel` の publish ログが出る

---

## 4. Action: Fibonacci

### 目的

長時間処理における `Goal` / `Feedback` / `Result` の 3 段階を確認する。

### 用途例（ロボット）

- ナビゲーション到達、アーム把持、ドッキングなど数秒以上かかるタスク
- 「目標地点へ移動」を Goal で依頼し、進捗を Feedback、完了可否を Result で受ける

### 実行

端末 1:
```bash
docker compose exec ros2_dev bash -lc "source /opt/ros/humble/setup.bash && cd /root/ros2_ws && source install/setup.bash && ros2 run py_robot_lab fibonacci_action_server"
```

端末 2:
```bash
docker compose exec ros2_dev bash -lc "source /opt/ros/humble/setup.bash && cd /root/ros2_ws && source install/setup.bash && ros2 run py_robot_lab fibonacci_action_client 12"
```

### 成功条件

- Server 側に `/fibonacci` の待受ログが表示される
- Client 側で `Goal accepted` が表示される
- Client 側で `Feedback` が段階的に更新される
- 最後に `Result` が表示される

---

## 5. Parameter: runtime tuning

### 目的

実行中ノードの設定値を `ros2 param set` で更新し、挙動が変わることを確認する。

### 用途例（ロボット）

- 実機テスト中に制御ゲイン、しきい値、安全距離、ログ周期を再起動なしで調整
- 障害物回避の閾値を現場で調整し、即時に挙動をチューニング

### 実行

端末 1:
```bash
docker compose exec ros2_dev bash -lc "source /opt/ros/humble/setup.bash && cd /root/ros2_ws && source install/setup.bash && ros2 run py_robot_lab param_monitor"
```

端末 2（文字列パラメータ変更）:
```bash
docker compose exec ros2_dev bash -lc "source /opt/ros/humble/setup.bash && ros2 param set /param_monitor message 'hello parameter'"
```

端末 2（周期パラメータ変更）:
```bash
docker compose exec ros2_dev bash -lc "source /opt/ros/humble/setup.bash && ros2 param set /param_monitor log_period_sec 0.5"
```

### 成功条件

- 端末 1 で `message="..." period=...` が定期表示される
- `message` 変更時に表示文字列が更新される
- `log_period_sec` 変更時に表示間隔が変わる

---

## License

`py_robot_lab` の `package.xml` に合わせ、Apache License 2.0 を想定しています。  
公開時はルートに `LICENSE` ファイルを追加してください。