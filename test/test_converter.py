# Copyright (c) 2023 TIER IV.inc
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

import autoware_auto_vehicle_msgs.msg as auto_vechile
import autoware_vehicle_msgs.msg as aw_vehicloe
from builtin_interfaces.msg import Time
from rclpy.clock import Clock
from rosbag2_py import TopicMetadata

from autoware_msg_bag_converter.converter import change_topic_type
from autoware_msg_bag_converter.converter import convert_msg


def get_time_now() -> Time:
    stamp = Clock().now()
    return stamp.to_msg()


def test_change_topic_type() -> None:
    old_type = TopicMetadata(
        name="/vehicle/status/control_mode",
        type="autoware_auto_vehicle_msgs/msg/ControlModeReport",
        serialization_format="cdr",
    )
    new_type = change_topic_type(old_type)
    assert new_type.name == "/vehicle/status/control_mode"
    assert new_type.type == "autoware_vehicle_msgs/msg/ControlModeReport"
    assert new_type.serialization_format == "cdr"


def test_convert_msg() -> None:
    now = get_time_now()
    auto_control_report = auto_vechile.ControlModeReport(
        stamp=now,
        mode=auto_vechile.ControlModeReport.AUTONOMOUS,
    )
    aw_control_report = convert_msg(auto_control_report)
    assert aw_control_report == aw_vehicloe.ControlModeReport(
        stamp=now,
        mode=aw_vehicloe.ControlModeReport.AUTONOMOUS,
    )
