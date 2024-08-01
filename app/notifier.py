import boto3
import time
from twilio.rest import Client
from .config import aws_access_key_id, aws_secret_access_key, region_name, sns_topic_arn, SNS_ENABLED

# Initialize the SNS client
sns_client = boto3.client(
    'sns',
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name=region_name
)

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
            # send SNS notification
            if SNS_ENABLED:
                response = sns_client.publish(
                    TopicArn=sns_topic_arn,
                    Message=message,
                    Subject=subject
                )

            # Start cooldown period
            last_notification_time = current_time  # Update the last notification time
            print(f"Notification sent: {response['MessageId']}")
        except Exception as e:
            print(f"Error sending notification: {str(e)}")
    else:
        print("Cooldown period active. No notification sent.")
