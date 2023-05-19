import requests
import subprocess
import json
import os

# Load the saved API key
with open('~/.myapp/api_key_file', 'r') as f:
    api_key = f.read().strip()

# Ping the server
response = requests.get('http://<your_backend_endpoint>/daemon_check', headers={'X-Api-Key': api_key})

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