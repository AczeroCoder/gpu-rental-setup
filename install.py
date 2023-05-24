import requests
import getpass
import os
import subprocess

def get_machine_id():
    with open('/etc/machine-id') as f:
        return f.read().strip()

# Send the details to your server
getUID = get_machine_id()
response1 = requests.post('https://3f07-2a02-c7e-2818-f900-5076-55ee-5fc7-a963.ngrok-free.app/get_api_key', headers={'getKey': getUID})

if response1.status_code == 200:
    api_key = response1.json()['api_key']
    gpu_details = {}
    print("Getting all key information such as GPU names, IDs, CPU, Motherboard, etc")
    gpu_details['gpu_model'] = input('Do you wish to download (SOFTWARE): ')
    # gpu_details['vram'] = input('Enter your VRAM: ')
    # gpu_details['rent_price'] = input('Enter the rent price: ')

    response = requests.post('https://3f07-2a02-c7e-2818-f900-5076-55ee-5fc7-a963.ngrok-free.app/add_gpu', headers={'X-Api-Key': api_key}, json=gpu_details)

    if response.status_code == 200:
        print('GPU details submitted successfully.')

        # Download the daemon
        if os.path.exists("gpureq.py"):
            os.remove("gpureq.py")
        subprocess.run(["wget", "https://raw.githubusercontent.com/AczeroCoder/gpu-rental-setup/main/gpureq.py"])

        # Make the daemon file executable
        subprocess.run(["chmod", "+x", "gpureq.py"])

        # Schedule the daemon to run every 30 seconds
        crontab_line = "*/30 * * * * /usr/bin/python3 ~/.myapp/gpureq.py"
        with open("/etc/crontab", "a") as cron_file:
            cron_file.write(crontab_line)

    else:
        print(f'Error: {response.status_code}. {response.text}')
else:
    print(f'Error: {response1.status_code}. {response1.text}')
