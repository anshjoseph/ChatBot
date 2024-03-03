import json
import requests
from urllib.parse import quote 


# load config
config:dict = None
with open('run_service.conf','r') as file:
    config = json.load(file)

config_API = config.get('API')


API_ADDR = f"http://{config_API.get('host')}:{config_API.get('port')}/{config_API.get('version')}/ask"

def check_api():
    message = "hello"
    url = API_ADDR +"?message=" +quote(message, safe='')
    result = requests.post(url)
    assert result.status_code == 200
