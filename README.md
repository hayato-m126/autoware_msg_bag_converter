# autoware_msg_bag_converter

This package converts bag containing type autoware_auto_msg to autoware_msg.

## preparation

1. create ros2 workspace for converter (ex. $HOME/ros_ws/converter)
2. clone this repository into converter workspace
3. clone dependency repos
4. build converter workspace

Example command is below.

```shell
mkdir -p $HOME/ros_ws/converter/src
cd $HOME/ros_ws/converter/src
git clone https://github.com/autowarefoundation/autoware_msg_bag_converter.git
cd autoware_msg_bag_converter
vcs import .. < dependency.repos
cd $HOME/ros_ws/converter
colcon build --symlink-install --cmake-args -DCMAKE_EXPORT_COMPILE_COMMANDS=ON -DCMAKE_BUILD_TYPE=Release
```

## usage

```shell
cd $HOME/ros_ws/converter
source install/setup.bash
cd src/autoware_msg_bag_converter/autoware_msg_bag_converter

# convert one bag
python3 main.py ${input_bag} ${output_bag}

# convert multi bags in directory
python3 main.py ${input_bag_dir} ${output_bag_dir} -d
```

## demo

~~convert the [tutorial](https://autowarefoundation.github.io/autoware-documentation/main/tutorials/ad-hoc-simulation/rosbag-replay-simulation/) bag file.~~
Conversion is not necessary because the bag has been uploaded already changed to autoware_msg since 6/7/2024

![demo](./demo.gif)
