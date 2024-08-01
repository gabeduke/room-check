import requests
import json
from .config import desired_dates, rooms_of_interest, headers, debug, trace

def fetch_availability():
    desired_dates.sort()
    start_date = desired_dates[0]
    end_date = desired_dates[-1]

    url = f"https://be-booking-engine-api.prodinnroad.com/availability?startDate={start_date}&endDate={end_date}&propertyId=680"

    response = requests.get(url, headers=headers)
    availability_data = []

    try:
        data = response.json()
        if trace:
            print("JSON Response:\n", json.dumps(data, indent=2))

        if isinstance(data, list):
            for room in data:
                room_name = room.get('name')
                if room_name in rooms_of_interest:
                    room_info = {'name': room_name, 'availability': []}
                    for rate in room.get('rates', []):
                        date = rate.get('effectiveDate').split('T')[0]
                        if date in desired_dates:
                            availability = rate.get('isRoomAvailable')
                            price = rate.get('baseAfterTax', {}).get('value')
                            room_info['availability'].append({
                                'date': date,
                                'is_available': availability,
                                'price': price
                            })
                            # Optional: handle notifications here or elsewhere
                    availability_data.append(room_info)
        else:
            print(f"Error: Unexpected data format or error message: {data.get('message', 'Unknown error')}")
    except json.JSONDecodeError:
        print("Error: Unable to decode the response as JSON.")
        print("Response content:")
        print(response.text)

    return availability_data  # Return the data
