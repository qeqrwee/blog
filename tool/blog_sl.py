import os
from os import mkdir
import json

data_file = os.path.join(os.path.dirname(__file__),'..','data','blogs.txt')

def load_blogs():
    if not os.path.exists(data_file):
        return []
    else:
        with open(data_file,"r",encoding="UTF-8") as f:
            return json.loads(f.read())

def save_blogs(blogs):
    if not os.path.exists(data_file):
        mkdir(os.path.dirname(data_file))
    with open(data_file,"w",encoding="UTF-8") as f:
        f.write(json.dumps(blogs,ensure_ascii=False,indent=2))