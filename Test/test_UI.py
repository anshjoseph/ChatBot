import json
import requests
from urllib.parse import quote 


# load config
config:dict = None
with open('run_service.conf','r') as file:
    config = json.load(file)

config_UI = config.get('UI')


API_ADDR = f"http://{config_UI.get('host')}:{config_UI.get('port')}/"

def check_api():
    result = requests.get(API_ADDR)
    assert result.status_code == 200
