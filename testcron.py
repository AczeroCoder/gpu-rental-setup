import requests
import time

# URL of your backend
backend_url = 'https://27a2-90-211-254-60.ngrok-free.app/daemon_check'

while True:
    try:
        response = requests.get(backend_url)
        data = response.json()
        print(data)
#         if 'type' in data and data['type'] == 'PING':
#             print('Received PING from server.')
#         else:
#             print('Unexpected response from server:', data)
    except requests.exceptions.RequestException as e:
        print('Error while sending request:', e)

    # Sleep for 30 seconds
    time.sleep(30)
