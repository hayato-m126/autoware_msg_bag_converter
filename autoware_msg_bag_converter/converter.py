# Copyright (c) 2024 TIER IV.inc
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# refer the test code of rosbag2_py
# https://github.com/ros2/rosbag2/blob/rolling/rosbag2_py/test/test_sequential_writer.py
# https://github.com/ros2/rosbag2/blob/rolling/rosbag2_py/test/test_reindexer.py

from pathlib import Path
from typing import TYPE_CHECKING

from autoware_control_msgs.msg import Control
from autoware_control_msgs.msg import Lateral
from autoware_control_msgs.msg import Longitudinal
from autoware_planning_msgs.msg import PathPoint
from rclpy.serialization import deserialize_message
from rclpy.serialization import serialize_message
from rosbag2_py import Reindexer
from rosbag2_py import TopicMetadata
from rosidl_runtime_py.utilities import get_message
from tier4_planning_msgs.msg import PathPointWithLaneId
from tier4_planning_msgs.msg import PathWithLaneId as T4PathWithLaneId

from autoware_msg_bag_converter.bag import create_reader
from autoware_msg_bag_converter.bag import create_writer
from autoware_msg_bag_converter.bag import get_storage_options

if TYPE_CHECKING:
    from autoware_auto_control_msgs.msg import AckermannControlCommand
    from autoware_auto_planning_msgs.msg import PathWithLaneId as AutoPathWithLaneId

TYPES_NOT_SIMPLY_REPLACED = {
    "autoware_auto_control_msgs/msg/AckermannControlCommand": "autoware_control_msgs/msg/Control",
    "autoware_auto_planning_msgs/msg/PathWithLaneId": "tier4_planning_msgs/msg/PathWithLaneId",
}

# Define the type of message you want autoware prefixes to be attached to (forward matching)
TYPES_TO_ADD_AUTOWARE_PREFIX = [
    "control_validator/msg",
    "planning_validator/msg",
    "vehicle_cmd_gate/msg",
]


def change_topic_type(old_type: TopicMetadata) -> TopicMetadata:
    if old_type.type in TYPES_NOT_SIMPLY_REPLACED:
        return TopicMetadata(
            name=old_type.name,
            type=TYPES_NOT_SIMPLY_REPLACED[old_type.type],
            serialization_format="cdr",
        )
    if any(old_type.type.startswith(prefix) for prefix in TYPES_TO_ADD_AUTOWARE_PREFIX):
        return TopicMetadata(
            name=old_type.name,
            type=f"autoware_{old_type.type}",
            serialization_format="cdr",
        )
    # If old_type is not in the conversion rules, simply remove "auto_" and use that as the new type.
    return TopicMetadata(
        name=old_type.name,
        type=old_type.type.replace("autoware_auto_", "autoware_"),
        serialization_format="cdr",
    )


def convert_msg(topic_name: str, msg: bytes, type_map: dict) -> bytes:
    # get old msg type
    old_type: str = type_map[topic_name]
    if old_type not in TYPES_NOT_SIMPLY_REPLACED:
        return msg
    old_msg = deserialize_message(
        msg,
        get_message(type_map[topic_name]),
    )
    if old_type == "autoware_auto_control_msgs/msg/AckermannControlCommand":
        old_msg: AckermannControlCommand
        lateral = Lateral(
            stamp=old_msg.lateral.stamp,
            steering_tire_angle=old_msg.lateral.steering_tire_angle,
            steering_tire_rotation_rate=old_msg.lateral.steering_tire_rotation_rate,
            is_defined_steering_tire_rotation_rate=True,
        )
        longitudinal = Longitudinal(
            stamp=old_msg.longitudinal.stamp,
            velocity=old_msg.longitudinal.speed,
            acceleration=old_msg.longitudinal.acceleration,
            jerk=old_msg.longitudinal.jerk,
            is_defined_acceleration=True,
            is_defined_jerk=False,
        )
        return serialize_message(
            Control(
                stamp=old_msg.stamp,
                lateral=lateral,
                longitudinal=longitudinal,
            ),
        )
    if old_type == "autoware_auto_planning_msgs/msg/PathWithLaneId":
        old_msg: AutoPathWithLaneId
        points: list[PathPointWithLaneId] = []
        for old_point in old_msg.points:
            point = PathPoint(
                pose=old_point.point.pose,
                longitudinal_velocity_mps=old_point.point.longitudinal_velocity_mps,
                lateral_velocity_mps=old_point.point.lateral_velocity_mps,
                heading_rate_rps=old_point.point.heading_rate_rps,
                is_final=old_point.point.is_final,
            )
            points.append(PathPointWithLaneId(point=point, lane_ids=old_point.lane_ids))
        return serialize_message(
            T4PathWithLaneId(
                header=old_msg.header,
                points=points,
                left_bound=old_msg.left_bound,
                right_bound=old_msg.right_bound,
            ),
        )
    return None


def convert_bag(input_bag_path: str, output_bag_path: str) -> None:
    p_input = Path(input_bag_path)
    storage_type = "mcap"
    for _ in p_input.glob("*.db3"):
        storage_type = "sqlite3"
        break
    # open reader
    reader = create_reader(input_bag_path, storage_type)
    # open writer
    writer = create_writer(output_bag_path, storage_type)

    # create topic
    type_map = {}  # key: topic_name value: old_type's msg type
    for topic_type in reader.get_all_topics_and_types():
        type_map[topic_type.name] = topic_type.type
        new_topic_type = change_topic_type(
            topic_type,
        )
        writer.create_topic(new_topic_type)

    # copy data from input bag to output bag
    while reader.has_next():
        topic_name, msg, stamp = reader.read_next()
        new_msg = convert_msg(topic_name, msg, type_map)
        writer.write(topic_name, new_msg, stamp)

    # reindex to update metadata.yaml
    del writer
    Reindexer().reindex(get_storage_options(output_bag_path, storage_type))
