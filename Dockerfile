FROM ros:humble-ros-base

# create workspace
RUN mkdir -p /ros_ws/src
WORKDIR /ros_ws/

# clone projects
RUN cd src && git clone https://github.com/chenjunnn/rm_auto_aim --depth=1 && \
    git clone https://github.com/chenjunnn/ros2_mindvision_camera --depth=1 && \
    git clone https://github.com/chenjunnn/ros2_hik_camera --depth=1 && \
    git clone https://github.com/chenjunnn/rm_gimbal_description --depth=1 && \
    git clone https://github.com/chenjunnn/rm_serial_driver --depth=1 && \
    git clone https://github.com/chenjunnn/rm_vision --depth=1

# install dependencies and some tools
RUN apt-get update && rosdep install --from-paths src --ignore-src -r -y && \
    apt-get install ros-humble-foxglove-bridge wget htop vim -y && \
    rm -rf /var/lib/apt/lists/*

# setup zsh
RUN sh -c "$(wget -O- https://github.com/deluan/zsh-in-docker/releases/download/v1.1.2/zsh-in-docker.sh)" -- \
    -t jispwoso -p git \
    -p https://github.com/zsh-users/zsh-autosuggestions \
    -p https://github.com/zsh-users/zsh-syntax-highlighting && \
    chsh -s /bin/zsh && \
    rm -rf /var/lib/apt/lists/*

# build
RUN . /opt/ros/humble/setup.sh && colcon build --symlink-install --cmake-args -DCMAKE_BUILD_TYPE=Release

# setup .zshrc
RUN echo 'export TERM=xterm-256color\n\
source /ros_ws/install/setup.zsh\n\
eval "$(register-python-argcomplete3 ros2)"\n\
eval "$(register-python-argcomplete3 colcon)"\n'\
>> /root/.zshrc

# source entrypoint setup
RUN sed --in-place --expression \
      '$isource "/ros_ws/install/setup.bash"' \
      /ros_entrypoint.sh
