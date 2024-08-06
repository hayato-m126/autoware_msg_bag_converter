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

import argparse
from os.path import expandvars
from pathlib import Path
import re

from autoware_msg_bag_converter.converter import convert_bag

EXAMPLE_MESSAGE = """
# example
$ tree
bag_root # <- input_bag_dir_root
├── sample_mcap # <- input_bag_dir
│    ── metadata.yaml
│   └── sample_mcap_0.db3
└── sample_sqlite3 # <- input_bag_dir
    ├── metadata.yaml
    └── sample_sqlite3_0.db3
"""


def convert_bag_in_directory(input_dir: str, output_dir: str) -> None:
    input_root = Path(input_dir)
    output_root = Path(output_dir)

    pattern = re.compile(r".*\.(db3|mcap)$")
    bag_paths = [p for p in input_root.rglob("*") if pattern.match(str(p))]
    for db3_or_mcap_path in bag_paths:
        input_bag_dir = db3_or_mcap_path.parent
        rel_path = input_bag_dir.relative_to(input_root)
        output_bag_dir = output_root.joinpath(rel_path)
        convert_bag(input_bag_dir.as_posix(), output_bag_dir.as_posix())


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="path of input bag directory with autoware_auto_msgs")
    parser.add_argument("output", help="path of output bag directory with autoware_msgs")
    parser.add_argument(
        "--directory",
        "-d",
        action="store_true",
        help="If this option is specified, all rosbags under the directory specified in input will be converted",
    )
    args = parser.parse_args()
    if not Path(args.input).is_dir():
        print(f"{args.input=} is not directory")  # noqa
        print(EXAMPLE_MESSAGE)  # noqa
        return
    if not args.directory:
        convert_bag(expandvars(args.input), expandvars(args.output))
    else:
        convert_bag_in_directory(expandvars(args.input), expandvars(args.output))


if __name__ == "__main__":
    main()
