import requests
import getpass
import os
import subprocess

def get_machine_id():
    with open('/etc/machine-id') as f:
        return f.read().strip()

api_key = getpass.getpass('Please enter your API key: ')
gpu_details = {}  # Assuming this is the format you want
gpu_details['gpu_model'] = input('Enter your GPU Model: ')
gpu_details['vram'] = input('Enter your VRAM: ')
gpu_details['rent_price'] = input('Enter the rent price: ')

# Send the details to your server
response = requests.post('https://3f07-2a02-c7e-2818-f900-5076-55ee-5fc7-a963.ngrok-free.app/add_gpu', headers={'X-Api-Key': api_key}, json=gpu_details)

if response.status_code == 200:
    print('GPU details submitted successfully.')
    # If API key is valid, save it for future requests
    with open('~/.myapp/api_key_file', 'w') as f:
        f.write(api_key)

    # Download the daemon
    subprocess.run(["wget", "https://github.com/AczeroCoder/gpu-rental-setup/blob/main/daemon.py"])

    # Make the daemon file executable
    subprocess.run(["chmod", "+x", "daemon.py"])

    # Schedule the daemon to run every 30 seconds
    crontab_line = "*/30 * * * * /usr/bin/python3 ~/.myapp/daemon.py"
    with open("/etc/crontab", "a") as cron_file:
        cron_file.write(crontab_line)

else:
    print(f'Error: {response.status_code}. {response.text}')
