import rclpy
from rclpy.node import Node
from kr_msgs.msg import JogLinear
import paho.mqtt.client as mqtt
from rclpy.time import Time


class JogLinearSubscriber(Node):

    def __init__(self):
        super().__init__('jog_linear_subscriber')
        self.publisher_ = self.create_publisher(JogLinear, "/kr/motion/jog_linear", 10)
        self.velocity_x = 0.0
        self.velocity_y = 0.0
        self.velocity_z = 0.0
        self.velocity_rx = 0.0
        self.velocity_ry = 0.0
        self.velocity_rz = 0.0
        self.tmx = self.get_clock().now().nanoseconds/(1000*1000*1000)
        self.tmy = self.get_clock().now().nanoseconds/(1000*1000*1000)
        self.tmz = self.get_clock().now().nanoseconds/(1000*1000*1000)
        self.tmrx = self.get_clock().now().nanoseconds/(1000*1000*1000)
        self.tmry = self.get_clock().now().nanoseconds/(1000*1000*1000)
        self.tmrz = self.get_clock().now().nanoseconds/(1000*1000*1000)

        # MQTT setup
        self.mqtt_client = mqtt.Client()
        self.mqtt_client.username_pw_set("kr2", "joker")
        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.on_message = self.on_message
        self.mqtt_client.connect("10.6.6.6", 1883)
        self.mqtt_client.loop_start()

        # Timer to publish jog linear messages
        timer_period = 0.002  # seconds
        self.timer = self.create_timer(timer_period, self.jog_linear_callback)

    def on_connect(self, client, userdata, flags, rc):
        print("Connected to MQTT Broker!")
        client.subscribe("robot/velocity/x")
        client.subscribe("robot/velocity/y")
        client.subscribe("robot/velocity/z")
        client.subscribe("robot/velocity/rx")
        client.subscribe("robot/velocity/ry")
        client.subscribe("robot/velocity/rz")


    def on_message(self, client, userdata, msg):
        current_time = self.get_clock().now().nanoseconds/(1000*1000*1000)  # Get current time in seconds

        try:
            value = float(msg.payload.decode())
        except ValueError:
            print(f"Invalid data received on {msg.topic}: {msg.payload.decode()}")
            return

        if msg.topic == "robot/velocity/x":
            self.velocity_x = value
            self.tmx = current_time

        elif msg.topic == "robot/velocity/y":
            self.velocity_y = value
            self.tmy = current_time

        elif msg.topic == "robot/velocity/z":
            self.velocity_z = value
            self.tmz = current_time

        elif msg.topic == "robot/velocity/rx":
            self.velocity_rx = value
            self.tmrx = current_time

        elif msg.topic == "robot/velocity/ry":
            self.velocity_ry = value
            self.tmry = current_time

        elif msg.topic == "robot/velocity/rz":
            self.velocity_rz = value
            self.tmrz = current_time

        print(f"Updated Velocities -> X: {self.velocity_x}, Y: {self.velocity_y}, Z: {self.velocity_z}")

    def jog_linear_callback(self):
        current_time = self.get_clock().now().nanoseconds/(1000*1000*1000) # Current time in seconds

        # Timeout threshold in seconds
        timeout =0.5
        print(current_time)
        print(timeout)
        print(f"{self.tmx}+{self.tmy}+{self.tmz}")

        # Check if we should reset velocities
        if current_time - self.tmx > timeout:
            self.velocity_x = 0.0
            self.mqtt_client.publish("robot/velocity/x", self.velocity_x)
        if current_time - self.tmy > timeout:
            self.velocity_y = 0.0
            self.mqtt_client.publish("robot/velocity/y", self.velocity_y)
        if current_time - self.tmz > timeout:
            self.velocity_z = 0.0
            self.mqtt_client.publish("robot/velocity/z", self.velocity_z)
        if current_time - self.tmrx > timeout:
            self.velocity_rx = 0.0
            self.mqtt_client.publish("robot/velocity/rx", self.velocity_rx)
        if current_time - self.tmry > timeout:
            self.velocity_ry = 0.0
            self.mqtt_client.publish("robot/velocity/ry", self.velocity_ry)
        if current_time - self.tmrz > timeout:
            self.velocity_rz = 0.0
            self.mqtt_client.publish("robot/velocity/rz", self.velocity_rz)

        msg = JogLinear()
        msg.vel = [self.velocity_x, self.velocity_y, self.velocity_z]
        msg.rot = [self.velocity_rx, self.velocity_ry, self.velocity_rz]

        self.publisher_.publish(msg)

        print(f"Publishing JOG LINEAR -> X: {self.velocity_x}, Y: {self.velocity_y}, Z: {self.velocity_z}")
        print(f"Publishing JOG LINEAR -> X: {self.velocity_rx}, Y: {self.velocity_ry}, Z: {self.velocity_rz}")


def main(args=None):
    rclpy.init(args=args)
    jog_linear_subscriber = JogLinearSubscriber()
    rclpy.spin(jog_linear_subscriber)
    jog_linear_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
