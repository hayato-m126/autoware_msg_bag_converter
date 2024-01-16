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
git clone https://github.com/hayato-m126/autoware_msg_bag_converter.git # to be updated
cd autoware_msg_bag_converter
vcs import .. < depedency.repos
cd $HOME/ros_ws/converter
colcon build --symlink-install --cmake-args -DCMAKE_EXPORT_COMPILE_COMMANDS=ON -DCMAKE_BUILD_TYPE=Release
```

## usage

TODO

```shell
ros2 run autoware_msg_bag_converter converter ${data_dir}
```

## demo

TODO
