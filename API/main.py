from fastapi import FastAPI, APIRouter
import os
import openai
import uvicorn
import chromadb
import json

# load config
config:dict = None
with open('run_service.conf','r') as file:
    config = json.load(file)
config_DB = config.get('DB')
config_API = config.get('API')


app = FastAPI()
openai.api_key = os.getenv("OPENAI_KEY")
class ChatBotInterface():
    def __init__(self) -> None:
        self.__version = config_API.get('version')
        self.__chroma_client = chromadb.PersistentClient()
        self.__messages = [{"role": "system", "content": "You are a helpful health assistant."}]
        self.__limit = 6
        self.__collection = self.__chroma_client.get_collection(config_DB.get('collection_name'))
        self.router = APIRouter()
        self.router.add_api_route(f"/{self.__version}/ask", self.post, methods=["POST"])
    def post(self,message:str):
        _data = self.__collection.query(
            query_texts=[message],
            n_results=config_DB.get('doc_ret'),
        )
        assert _data != None
        assert len(self.__messages) <= self.__limit
        _data = "".join(_data.get("documents")[0])
        self.__messages.append({"role": "user", "content": f"{_data} \n[message] answer my question from above data and make it crisp and make it short and classiy"})
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=self.__messages
        )
        # DEBUG
        if config_API.get('debug'):
            print(message)
            print(response['choices'][0]['message']['content'])
        return {'response':response['choices'][0]['message']['content'],'limit':self.__limit,'used':len(self.__messages)}

chatbot = ChatBotInterface()
app.include_router(chatbot.router)

if __name__ == "__main__":
    uvicorn.run("main:app", host=config_API.get('host'), reload=True, port=config_API.get('port'))


