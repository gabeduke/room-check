import os

desired_dates = os.getenv('DESIRED_DATES', '2025-06-29,2025-06-30,2025-07-01,2025-07-02,2025-07-03,2025-07-04,2025-07-05').split(',')
rooms_of_interest = ['Lake Front Bedroom', 'Lake Front Studio', 'Lake Front Suite', 'Lake Front Town House']
INTERVAL = int(os.getenv('INTERVAL', 3600))
SNS_ENABLED = os.getenv('SNS_ENABLED', 'false').lower() == 'true'
MQTT_ENABLED = os.getenv('MQTT_ENABLED', 'false').lower() == 'true'
mqtt_broker = 'mqtt.leetserve.com'
mqtt_port = 1883
mqtt_topic = 'home/general/alerts'
PORT = int(os.getenv('PORT', 5000))


headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-US',
    'cache-control': 'no-cache',
    'origin': 'https://lochlevenlodge.client.innroad.com',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://lochlevenlodge.client.innroad.com/',
    'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-platform': '"Android"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'cross-site',
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Mobile Safari/537.36'
}

debug = os.getenv('DEBUG', 'false').lower() == 'true'
print(f"Debug mode is {'on' if debug else 'off'}")
trace = os.getenv('TRACE', 'false').lower() == 'true'
print(f"trace mode is {'on' if trace else 'off'}")

# Retrieve AWS credentials and region from environment variables
aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
region_name = os.getenv('AWS_REGION', 'us-east-1')
sns_topic_arn = os.getenv('SNS_TOPIC_ARN')
