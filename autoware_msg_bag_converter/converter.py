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


def convert(self):
    # open reader
    reader, _, _ = self.__create_reader()
    # open writer
    writer, storage_options, _ = self.__create_writer()

    # first, write topic before write rosbag
    topic_type_list = {}
    for topic_type in reader.get_all_topics_and_types():
        topic_type_list[topic_type.name] = topic_type.type
        if topic_type.name in list(self.__convert_dict.keys()):
            topic_type = rosbag2_py.TopicMetadata(
                name=self.__convert_dict[topic_type.name][0],
                type=self.__convert_dict[topic_type.name][1],
                serialization_format="cdr",
                offered_qos_profiles=topic_type.offered_qos_profiles,
            )
        writer.create_topic(topic_type)

    self.__convert_qos_file()

    # convert topic and write to output bag
    while reader.has_next():
        topic_name, msg, stamp = reader.read_next()
        topic_name, msg = self.__convert_iv_topic(topic_name, msg, topic_type_list)
        if topic_name not in SKIP_TOPIC_LIST:
            writer.write(topic_name, msg, stamp)
    # reindex to update metadata.yaml
    del writer
    rosbag2_py.Reindexer().reindex(storage_options)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="path of input bag with autoware_auto_msgs")
    parser.add_argument("output", help="path of output bag with autoweare_msgs")
    args = parser.parse_args()
    convert(expandvars(args.input), expandvars(args.output))


if __name__ == "__main__":
    main()
