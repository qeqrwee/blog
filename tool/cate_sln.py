import os
import json
CATEGORY_DATA_FILE = os.path.join(os.path.dirname(__file__), '..','data', 'categories.txt')
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