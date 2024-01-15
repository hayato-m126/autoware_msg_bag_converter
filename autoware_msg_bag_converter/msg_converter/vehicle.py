# Copyright (c) 2024TIER IV.inc
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


import autoware_auto_vehicle_msgs.msg as auto
import autoware_vehicle_msgs.msg as aw


def control_mode_report(
    old: auto.ControlModeReport,
) -> aw.ControlModeReport:
    return aw.ControlModeReport(stamp=old.stamp, mode=old.mode)


def gear_report(old: auto.GearReport) -> aw.GearReport:
    return aw.GearReport(stamp=old.stamp, report=old.report)


def steering_report(old: auto.SteeringReport) -> aw.SteeringReport:
    return aw.SteeringReport(
        stamp=old.stamp, steering_tire_angle=old.steering_tire_angle
    )


def velocity_report(old: auto.VelocityReport) -> aw.VelocityReport:
    return aw.VelocityReport(
        header=old.header,
        longitudinal_velocity=old.longitudinal_velocity,
        lateral_velocity=old.lateral_velocity,
        heading_rate=old.heading_rate,
    )
