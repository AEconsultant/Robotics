import rclpy
from rclpy.node import Node
from kr_msgs.msg import JogLinear
import paho.mqtt.client as mqtt

class JogLinearSubscriber(Node):

    def __init__(self):
        super().__init__('jog_linear_subscriber')
        self.publisher_ = self.create_publisher(JogLinear, "/kr/motion/jog_linear", 10)
        self.velocity_x = 0.0

        # MQTT setup
        self.mqtt_client = mqtt.Client()
        self.mqtt_client.username_pw_set("kr2", "joker")
        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.on_message = self.on_message
        self.mqtt_client.connect("10.6.6.6", 1883)  # Replace with your MQTT broker
        self.mqtt_client.loop_start()

        # Timer to publish jog linear messages
        timer_period = 0.002  # seconds
        self.timer = self.create_timer(timer_period, self.jog_linear_callback)

    def on_connect(self, client, userdata, flags, rc):
        print("Connected to MQTT Broker!")
        client.subscribe("robot/velocity/x")  # Replace with your MQTT topic

    def on_message(self, client, userdata, msg):
        print(f"{msg.payload.decode()}")
        self.velocity_x = float(msg.payload.decode())
        print(f"Received velocity_x: {self.velocity_x}")

    def jog_linear_callback(self):
        msg = JogLinear()
        vel = [self.velocity_x, 0., 0.]
        rot = [0., 0., 0.]

        msg.vel = vel
        msg.rot = rot

        print(f"Publishing JOG LINEAR with velocity_x: {self.velocity_x}")
        self.mqtt_client.publish("robot/velocity/xin", "new message")
        self.publisher_.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    jog_linear_subscriber = JogLinearSubscriber()
    rclpy.spin(jog_linear_subscriber)
    jog_linear_subscriber.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
