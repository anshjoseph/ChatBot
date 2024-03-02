from fastapi import FastAPI
import uvicorn
import json
from fastapi.responses import HTMLResponse
import requests
from urllib.parse import quote 


# load config
config:dict = None
with open('run_service.conf','r') as file:
    config = json.load(file)
config_UI = config.get('UI')
config_API = config.get('API')


API_ADDR = f"http://{config_API.get('host')}:{config_API.get('port')}/{config_API.get('version')}/ask"
app = FastAPI()

@app.get("/")
def index():
    file_html = open(config_UI.get('base_file_html'),'r')
    data =  file_html.read()
    file_html.close()
    return HTMLResponse(data)
@app.post("/api/")
def get_data(message:str):
    url = API_ADDR +"?message=" +quote(message, safe='')
    result = requests.post(url)
    return json.loads(result.text)

if __name__ == "__main__":
    uvicorn.run("main:app", host=config_UI.get('host'), reload=config_UI.get('reload'), port=config_UI.get('port'))
