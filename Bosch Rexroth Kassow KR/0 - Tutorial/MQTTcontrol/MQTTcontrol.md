# Example code to control the Kassow robot using MQTT and the laptop keyboard

### Instal mosquitto MQTT Broker

#### Note: the example code was made with Mosquitto instaled in the ROS2 device

- In the ubuntu terminal run:

    sudo apt update -y && sudo apt install mosquitto mosquitto-clients -y

- Setup mosquito authentication requirements:

    sudo nano /etc/mosquitto/mosquitto.conf

    - In this file add this:

        listener 1883

        allow_anonymous false

        password_file /etc/mosquitto/passwd

- Setup mosquitto password access

    sudo mosquitto_passwd -c /etc/mosquitto/passwd username

- Restart mosquitto:

    sudo systemctl restart mosquitto


### Setup ROS2 code:

- Go to the ROS2 workpackage directory:

    cd ~/dew_ws/

- Input the code:

    sudo nano src/orange-ros2/kr_example/python/kr_example_python/kr_mqttjog.py

- Setup and entrypoint:

    - got to:

        sudo nano src/orange-ros2/kr_example/python/setup.py

    - In the entrypoint list, input:

        'mqtt_jog = kr_example_python.kr_mqttjog:main'

- Finaly Run:

    colcon build

    . install/setup.bash

- Now run the script with:

    ros2 run kr_example_python mqtt_jog


### Laptop Command:

- run the script "mqttKeyCommand.py"

- Press the numeric up(8) and down(2) keys.

