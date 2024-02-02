FROM fateryu/ros2_humble_openvino

USER root

# create workspace
RUN mkdir -p /ros_ws/src
WORKDIR /ros_ws/

# clone projects
RUN cd src && git clone https://github.com/FaterYU/rm_auto_aim --depth=1 && \
    git clone https://github.com/FaterYU/rm_buff --depth=1 && \
    git clone https://github.com/FaterYU/rm_vision_ros2_hik_camera --depth=1 && \
    git clone https://github.com/FaterYU/rm_gimbal_description --depth=1 && \
    git clone https://github.com/FaterYU/rm_serial_driver --depth=1 && \
    git clone https://github.com/FaterYU/rm_vision --depth=1

# install dependencies and some tools
RUN apt-get update && rosdep install --from-paths src --ignore-src -r -y && \
    apt-get install ros-humble-foxglove-bridge wget htop vim nano -y && \
    rm -rf /var/lib/apt/lists/*

# build
RUN . /opt/ros/humble/setup.sh && colcon build --symlink-install --cmake-args -DCMAKE_BUILD_TYPE=Release

# setup .zshrc
RUN echo 'source /ros_ws/install/setup.zsh' >> /root/.zshrc
RUN echo 'eval "$(register-python-argcomplete3 ros2)"' >> /root/.zshrc
RUN echo 'eval "$(register-python-argcomplete3 colcon)"' >> /root/.zshrc
