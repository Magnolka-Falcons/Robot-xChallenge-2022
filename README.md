# Robot-xChallenge2022

Robot code prepered fon xChallanege 2022 in Rszeszów. You can see some images [here](https://github.com/Magnolka-Falcons/Robot-xChallenge-2022/tree/master/images).

## Requirements:

- [ROS2](https://docs.ros.org/en/foxy/Installation.html)
- GPIO library

```bash
pip install RPi.GPIO
```


## Build package
To build package navigate to main package folder and run:

```bash
colcon build
```
## Run programm

#### Source fils:

```bash
. robot-xchallange-2022/install/setup.bash
```

#### Run sungle package:

```bash
ros2 run package_name executable_name
```
#### Package list:
- camera
    - camera
- drive_system
    - drive_system
- lift
    - lift_node


#### Run whole robot

```bash
    cd robot-xchallange-2022/ && ros2 launch launch.py
```


## Electronic parts

- Raspberry PI
- BLCD motors 4x
- DC motors 2x

## Render
![robot_render](/images/robot.png)