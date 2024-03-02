import chromadb
from glob import glob
import json
from uuid import uuid4

# load config
config:dict = None
with open('run_service.conf','r') as file:
    config = json.load(file)
config = config.get('DB')

print(config)
if config.get('store'):
    chroma_client = chromadb.PersistentClient()
else:
    chroma_client = chromadb.Client()
collection = chroma_client.create_collection(name=config.get('collection_name'))

def data_processor(data:str)->str:
    return data.replace('\n','').replace("\'",'')

def load_files(base_dir='./Docs/'):
    base_dir += "*.txt"
    load_files_loc = glob(base_dir)
    for idx,file_loc in enumerate(load_files_loc):
        doc_id = str(uuid4()) 
        file = open(file_loc,'r')
        # file data, file loc, file id, idx, total len
        yield (data_processor(file.read()),file_loc,doc_id,idx,len(load_files_loc))
        file.close()

load_files_gen = load_files()
print("START PROCESSING FILE")
for file_data in load_files_gen:
    file_data, file_loc, file_id, idx, total_len = file_data
    print(f"\tfile: {file_loc} is start processing with id: {file_id}")
    collection.add(
        documents=[file_data],
        metadatas=[{"source": file_loc}],
        ids=[file_id]
    )
    print(f"\tFILE: {file_loc} is finish processing with ID: {file_id}")
    print(f"\t----------{idx+1}/{total_len}------------")
print("FILE PROCESSING ID DONE")