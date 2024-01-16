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

import argparse
from os.path import expandvars

from autoware_msg_bag_converter.converter import convert_bag


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="path of input bag with autoware_auto_msgs")
    parser.add_argument("output", help="path of output bag with autoware_msgs")
    args = parser.parse_args()
    convert_bag(expandvars(args.input), expandvars(args.output))


if __name__ == "__main__":
    main()
