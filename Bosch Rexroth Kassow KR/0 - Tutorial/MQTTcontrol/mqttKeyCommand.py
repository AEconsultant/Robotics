import paho.mqtt.publish as publish
import keyboard
import threading
import time

# MQTT Broker Details
broker = "10.6.6.6"  # Replace with your MQTT broker address
port = 1883  # Default MQTT port
topicx = "robot/velocity/x"  # MQTT topic
topicy = "robot/velocity/y"  # MQTT topic
topicz = "robot/velocity/z"  # MQTT topic
topicrx = "robot/velocity/rx"  # MQTT topic
topicry = "robot/velocity/ry"  # MQTT topic
topicrz = "robot/velocity/rz"  # MQTT topic

# MQTT Authentication
user = "kr2"      # Replace with your username
pssw = "joker"  # Replace with your password

# Timer to detect inactivity
stop_timer = None


def reset_timer():
    """Reset the stop timer to publish 0 after 0.5 seconds of inactivity."""
    global stop_timer

    if stop_timer:
        stop_timer.cancel()  # Cancel the previous timer if it exists

    stop_timer = threading.Timer(0.1, publish_stop_signal)  # Start a new 0.5s timer
    stop_timer.start()

def publish_stop_signal():
    """Publish 0 to MQTT when no key is pressed for 0.5 seconds."""
    publish.single(topicx, 0, hostname=broker, port=port, auth={'username': user, 'password': pssw})
    publish.single(topicy, 0, hostname=broker, port=port, auth={'username': user, 'password': pssw})
    publish.single(topicz, 0, hostname=broker, port=port, auth={'username': user, 'password': pssw})
    publish.single(topicrx, 0, hostname=broker, port=port, auth={'username': user, 'password': pssw})
    publish.single(topicry, 0, hostname=broker, port=port, auth={'username': user, 'password': pssw})
    publish.single(topicrz, 0, hostname=broker, port=port, auth={'username': user, 'password': pssw})
    print("Published 0 to topic (timeout)")

def on_press(event):
    """Handle keyboard press events and publish MQTT messages."""
    if event.name == 'o':
        publish.single(topicx, 50, hostname=broker, port=port , auth={'username': user, 'password': pssw})
        print("Published +v to topic")
    elif event.name == 'l':
        publish.single(topicx, -50, hostname=broker, port=port , auth={'username': user, 'password': pssw})
        print("Published -v to topic")

    elif event.name == 'ç':
        publish.single(topicy, 50, hostname=broker, port=port , auth={'username': user, 'password': pssw})
        print("Published -v to topic")

    elif event.name == 'k':
        publish.single(topicy, -50, hostname=broker, port=port , auth={'username': user, 'password': pssw})
        print("Published -v to topic")

    elif event.name == 'p':
        publish.single(topicz, 50, hostname=broker, port=port , auth={'username': user, 'password': pssw})
        print("Published -v to topic")

    elif event.name == 'i':
        publish.single(topicz, -50, hostname=broker, port=port , auth={'username': user, 'password': pssw})
        print("Published -v to topic")
###
    elif event.name == 'w':
        publish.single(topicrx, 15, hostname=broker, port=port , auth={'username': user, 'password': pssw})
        print("Published -v to topic")

    elif event.name == 's':
        publish.single(topicrx, -15, hostname=broker, port=port , auth={'username': user, 'password': pssw})
        print("Published -v to topic")

    elif event.name == 'd':
        publish.single(topicry, 15, hostname=broker, port=port , auth={'username': user, 'password': pssw})
        print("Published -v to topic")

    elif event.name == 'a':
        publish.single(topicry, -15, hostname=broker, port=port , auth={'username': user, 'password': pssw})
        print("Published -v to topic")

    elif event.name == 'e':
        publish.single(topicrz, 15, hostname=broker, port=port , auth={'username': user, 'password': pssw})
        print("Published v to topic")

    elif event.name == 'q':
        publish.single(topicrz, -15, hostname=broker, port=port , auth={'username': user, 'password': pssw})
        print("Published -v to topic")

    #reset_timer()  # Reset the inactivity timer on each key press

def on_release(event):
    """Handle key release events and restart the timer to publish stop signal."""
    publish.single(topicx, 0, hostname=broker, port=port, auth={'username': user, 'password': pssw})
    publish.single(topicy, 0, hostname=broker, port=port, auth={'username': user, 'password': pssw})
    publish.single(topicz, 0, hostname=broker, port=port, auth={'username': user, 'password': pssw})
    #reset_timer()  # Start a 0.5s timer on key release

# Hook keyboard events
keyboard.on_press(on_press)
keyboard.on_release(on_release)

print("Press UP or DOWN arrow keys to publish messages to MQTT.")
print("Press 'ESC' to exit.")

# Keep the script running
keyboard.wait('esc')
