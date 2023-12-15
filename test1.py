import psutil
import json
import socket
from datetime import datetime

def check_service_status(service_name):
    for process in psutil.process_iter(['name']):
        if service_name.lower() in process.info['name'].lower():
            return "UP"
    return "DOWN"

def create_json_object(application_name, application_status, host_name):
    data = {
        'service_name': application_name,
        'service_status': application_status,
        'host_name': host_name
    }
    return data

# Configuration
services = ["httpd", "rabbitMQ", "postgreSQL"]

# Get the host name
host_name = socket.gethostname()

# Monitor services and create JSON object
service_status = "UP"

try:
    for service in services:
        if check_service_status(service) == "DOWN":
            service_status = "DOWN"
            json_object = create_json_object(service, service_status, host_name)
            file_path = service+"-"+service_status+"-"+ str(datetime.now().timestamp())+".json"
            with open(file_path,'w', encoding='utf-8') as json_file:
                json.dump(json_object,json_file)
except Exception as e:
    print(e)
finally:
    print("Code executed")



