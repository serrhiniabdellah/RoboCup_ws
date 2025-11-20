# Arduino Mega + ROS2 Bridge Setup

This guide helps you wire, upload, and run the Arduino Mega firmware with a ROS2 bridge. It includes Windows and Linux notes.

## Hardware Wiring

- Motor driver L298N
  - `D2` (PWM)  -> ENA (Left)
  - `D22` (DIR) -> IN1
  - `D23` (DIR) -> IN2
  - `D3` (PWM)  -> ENB (Right)
  - `D24` (DIR) -> IN3
  - `D25` (DIR) -> IN4
- Encoders
  - `D18` -> Left A (INT5)
  - `D19` -> Left B (INT4)
  - `D20` -> Right A (INT3)
  - `D21` -> Right B (INT2)
- E-Stop button -> `D26` (INPUT_PULLUP)

## Firmware Upload

1. Open `robocup_mega.ino` in Arduino IDE.
2. Board: Arduino Mega 2560.
3. Select serial port:
   - Windows: `COM3` (or similar)
   - Linux: `/dev/ttyACM0` or `/dev/ttyUSB0`
4. Upload.

## Serial Protocol

- Host -> Arduino (command velocity)
  - Frame: `[0xAA][0x01][float32 lin][float32 ang][0x55]`
- Host -> Arduino (9-channel command array)
  - Frame: `[0xAA][0x10][b0..b8][0x55]` where `bN` are signed int8 in `-127..127`
  - Mapping:
    - `b0`: left track power (-127..127)
    - `b1`: right track power (-127..127)
    - `b2`: rear flipper power
    - `b3`: front-right flipper down, `b4`: front-right up (combined)
    - `b5`: front-left flipper down, `b6`: front-left up (combined)
    - `b7`: camera up, `b8`: camera down (combined)
  - Current firmware: only `b0` and `b1` are applied to motors. Others are ignored unless additional pins are wired and code extended.
- Arduino -> Host (odometry)
  - Frame: `[0xAA][0x02][x][y][theta][vx][vtheta][0x55]` (5 x float32)
- Arduino -> Host (status)
  - Frame: `[0xAA][0x03][code][0x55]` where `code=0x00` means ESTOP

Little-endian floats are expected.

## Quick Serial Test (no ROS2)

Windows PowerShell:

```powershell
python .\src\robocup_simulation\scripts\test_arduino.py --port COM3 --baud 115200 --forward 0.2 --duration 3
```

Linux:

```bash
python3 src/robocup_simulation/scripts/test_arduino.py --port /dev/ttyACM0 --baud 115200 --forward 0.2 --duration 3
```

You should see ODOM prints as the robot moves.

## ROS2 Bridge

The bridge subscribes to `cmd_vel` and publishes `odom`, and optionally broadcasts `odom -> base_link` TF.

### Launch (Linux example)

```bash
source install/setup.bash
ros2 launch robocup_simulation arduino_navigation.launch.py serial_port:=/dev/ttyACM0
```

### Launch (Windows with ROS2)

```powershell
# 1) Source your ROS2 installation (adjust path):
# & "C:\dev\ros2_humble\local_setup.ps1"

# 2) Build this workspace (from repo root):
# colcon build --merge-install
# .\install\local_setup.ps1

# 3) Launch the bridge
ros2 launch robocup_simulation arduino_navigation.launch.py serial_port:=COM3
```

## Python Control GUI (no ROS2)

Run a simple Tkinter GUI that drives the 9-byte command array directly over serial.

Windows PowerShell:

```powershell
python -m pip install -r .\tools\python_interface\requirements.txt
python .\tools\python_interface\robot_control_gui.py
```

Use the Port dropdown (e.g., `COM3`), click Connect, then move the track sliders or use the arrow keys/WASD. Buttons are momentary for flippers and camera. Press E for emergency stop.

### Topics

- `/cmd_vel` (geometry_msgs/Twist) – input
- `/odom` (nav_msgs/Odometry) – output
- `/robot_status` (std_msgs/String) – status messages

## Tuning

Edit `Config.h` on Arduino:

- `WHEEL_SEPARATION` – axle length (m)
- `WHEEL_RADIUS` – wheel radius (m)
- `ENCODER_TICKS_PER_REV` – encoder resolution
- Max speeds: `MAX_LINEAR_SPEED`, `MAX_ANGULAR_SPEED`

## Troubleshooting

- No serial: try different COM port (Windows) or add udev permissions (Linux).
- Motors not moving: verify 12V supply and driver wiring; check `DEBUG_ENABLED`.
- Odom drift: calibrate wheel radius, separation, and ticks per rev.
