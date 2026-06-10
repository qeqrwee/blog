import os
import json

USER_DATA_FILE = os.path.join(os.path.dirname(__file__), '..','data', 'users.txt')

def load_users():
    """从TXT文件读取用户数据"""
    if not os.path.exists(USER_DATA_FILE):
        return []
    with open(USER_DATA_FILE, 'r', encoding='utf-8') as f:
        return json.loads(f.read())

def save_users(users):
    """将用户数据保存到TXT文件"""
    os.makedirs(os.path.dirname(USER_DATA_FILE), exist_ok=True)
    with open(USER_DATA_FILE, 'w', encoding='utf-8') as f:
        f.write(json.dumps(users, ensure_ascii=False, indent=2))