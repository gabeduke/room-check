import time

import boto3
import paho.mqtt.client as mqtt

from .config import (
    aws_access_key_id,
    aws_secret_access_key,
    region_name,
    sns_topic_arn,
    SNS_ENABLED,
    MQTT_ENABLED,
    mqtt_broker,
    mqtt_port,
    mqtt_topic,
)

# Initialize the SNS client
sns_client = boto3.client(
    'sns',
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name=region_name
)

# Initialize the MQTT client
mqtt_client = mqtt.Client()

# Set cooldown period in seconds (e.g., 3600 seconds for 1 hour)
COOLDOWN_PERIOD = 3600
last_notification_time = None


def notify_availability(room_name, date, price):
    global last_notification_time

    current_time = time.time()
    if last_notification_time is None or (current_time - last_notification_time) > COOLDOWN_PERIOD:
        message = f"Room {room_name} is available on {date} for ${price}."
        subject = "Room Availability Alert"

        try:
            # Send SNS notification
            if SNS_ENABLED:
                response = sns_client.publish(
                    TopicArn=sns_topic_arn,
                    Message=message,
                    Subject=subject
                )
                print(f"SNS Notification sent: {response['MessageId']}")

            # Send MQTT notification
            if MQTT_ENABLED:
                mqtt_client.connect(mqtt_broker, mqtt_port, 60)
                mqtt_client.publish(mqtt_topic, message)
                print("MQTT Notification sent")

            # Start cooldown period
            last_notification_time = current_time  # Update the last notification time
        except Exception as e:
            print(f"Error sending notification: {str(e)}")
    else:
        print("Cooldown period active. No notification sent.")

# MQTT message handling
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe(mqtt_topic)

def on_message(client, userdata, msg):
    print(f"Message received on topic {msg.topic}: {msg.payload.decode()}")

mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

# Start MQTT client loop
mqtt_client.connect(mqtt_broker, mqtt_port, 60)
mqtt_client.loop_start()
