import os
from os import mkdir
import json

data_file = os.path.join(os.path.dirname(__file__),'..','data','blogs.txt')
CATEGORY_DATA_FILE = os.path.join(os.path.dirname(__file__), '..','data', 'categories.txt')
USER_DATA_FILE = os.path.join(os.path.dirname(__file__), '..','data', 'users.txt')
COMMENT_DATA_FILE = os.path.join(os.path.dirname(__file__),'..','data', 'comments.txt')
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), '..','static', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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

def load_users():
    if not os.path.exists(USER_DATA_FILE):
        return []
    with open(USER_DATA_FILE, 'r', encoding='utf-8') as f:
        return json.loads(f.read())

def save_users(users):
    os.makedirs(os.path.dirname(USER_DATA_FILE), exist_ok=True)
    with open(USER_DATA_FILE, 'w', encoding='utf-8') as f:
        f.write(json.dumps(users, ensure_ascii=False, indent=2))

def load_categories():
    if not os.path.exists(CATEGORY_DATA_FILE):
        default_categories = [
            {"id": 1, "name": "技术笔记"},
            {"id": 2, "name": "生活随笔"},
            {"id": 3, "name": "学习心得"}
        ]
        save_categories(default_categories)
        return default_categories
    with open(CATEGORY_DATA_FILE, 'r', encoding='utf-8') as f:
        return json.loads(f.read())
def save_categories(categories):
    os.makedirs(os.path.dirname(CATEGORY_DATA_FILE), exist_ok=True)
    with open(CATEGORY_DATA_FILE, 'w', encoding='utf-8') as f:
        f.write(json.dumps(categories, ensure_ascii=False, indent=2))
def get_category_name(cate_id):
    categories = load_categories()
    cate = next((c for c in categories if c['id'] == cate_id), None)
    return cate['name'] if cate else '未分类'

def load_comments():
    if not os.path.exists(COMMENT_DATA_FILE):
        return []
    with open(COMMENT_DATA_FILE, 'r', encoding='utf-8') as f:
        return json.loads(f.read())


def save_comments(comments):
    os.makedirs(os.path.dirname(COMMENT_DATA_FILE), exist_ok=True)
    with open(COMMENT_DATA_FILE, 'w', encoding='utf-8') as f:
        f.write(json.dumps(comments, ensure_ascii=False, indent=2))