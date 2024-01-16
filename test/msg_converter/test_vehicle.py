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

from math import pi

import autoware_auto_vehicle_msgs.msg as auto
import autoware_vehicle_msgs.msg as aw
from builtin_interfaces.msg import Time
from rclpy.clock import Clock
from std_msgs.msg import Header

import autoware_msg_bag_converter.msg_converter.vehicle as msg_converter


def get_time_now() -> Time:
    stamp = Clock().now()
    return stamp.to_msg()


def test_control_mode_report() -> None:
    now = get_time_now()
    auto_msg = auto.ControlModeReport(stamp=now, mode=auto.ControlModeReport.AUTONOMOUS)
    aw_msg = msg_converter.control_mode_report(auto_msg)
    assert aw_msg == aw.ControlModeReport(
        stamp=now, mode=aw.ControlModeReport.AUTONOMOUS
    )


def test_gear_report() -> None:
    now = get_time_now()
    auto_msg = auto.GearReport(stamp=now, report=auto.GearReport.DRIVE)
    aw_msg = msg_converter.gear_report(auto_msg)
    assert aw_msg == aw.GearReport(stamp=now, report=aw.GearReport.DRIVE)


def test_steering_report() -> None:
    now = get_time_now()
    auto_msg = auto.SteeringReport(stamp=now, steering_tire_angle=pi / 2)
    aw_msg = msg_converter.steering_report(auto_msg)
    assert aw_msg == aw.SteeringReport(stamp=now, steering_tire_angle=pi / 2)


def test_velocity_report() -> None:
    header = Header(stamp=get_time_now(), frame_id="base_link")
    auto_msg = auto.VelocityReport(
        header=header,
        longitudinal_velocity=1.23,
        lateral_velocity=4.56,
        heading_rate=pi / 2,
    )
    aw_msg = msg_converter.velocity_report(auto_msg)
    assert aw_msg == aw.VelocityReport(
        header=header,
        longitudinal_velocity=1.23,
        lateral_velocity=4.56,
        heading_rate=pi / 2,
    )
