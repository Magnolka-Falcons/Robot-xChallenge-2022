from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription(
        [
            Node(
                package="drive_system",
                executable="drive_system",
            ),
            Node(
                package="camera",
                executable="camera",
            ),
        ]
    )