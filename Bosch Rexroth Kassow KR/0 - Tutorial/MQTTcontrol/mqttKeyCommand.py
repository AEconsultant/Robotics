import paho.mqtt.publish as publish
import keyboard
import threading

# MQTT Broker Details
broker = "10.6.6.6"  # Replace with your MQTT broker address
port = 1883  # Default MQTT port
topic = "robot/velocity/x"  # MQTT topic

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

    stop_timer = threading.Timer(0.5, publish_stop_signal)  # Start a new 0.5s timer
    stop_timer.start()

def publish_stop_signal():
    """Publish 0 to MQTT when no key is pressed for 0.5 seconds."""
    publish.single(topic, 0, hostname=broker, port=port, auth={'username': user, 'password': pssw})
    print("Published 0 to topic (timeout)")

def on_press(event):
    """Handle keyboard press events and publish MQTT messages."""
    if event.name == 'up':
        publish.single(topic, 25, hostname=broker, port=port , auth={'username': user, 'password': pssw})
        print("Published +v to topic")
    elif event.name == 'down':
        publish.single(topic, -25, hostname=broker, port=port , auth={'username': user, 'password': pssw})
        print("Published -v to topic")

    reset_timer()  # Reset the inactivity timer on each key press

def on_release(event):
    """Handle key release events and restart the timer to publish stop signal."""
    reset_timer()  # Start a 0.5s timer on key release

# Hook keyboard events
keyboard.on_press(on_press)
keyboard.on_release(on_release)

print("Press UP or DOWN arrow keys to publish messages to MQTT.")
print("Press 'ESC' to exit.")

# Keep the script running
keyboard.wait('esc')
