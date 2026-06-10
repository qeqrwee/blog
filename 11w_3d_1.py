from tool import blog_sl,user_sl,cate_sln,upload
from flask import Flask,render_template,request,url_for,redirect,session
from datetime import datetime,timedelta
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config.update(
    PERMANENT_SESSION_LIFETIME = timedelta(days=7),
    UPLOAD_FOLDER = upload.UPLOAD_FOLDER,
    SECRET_KEY = 'key'
)

@app.route('/')
def index():
    all_blogs = blog_sl.load_blogs()
    all_categories = cate_sln.load_categories()
    select_cate_id = request.args.get('cate_id')
    show_blog = all_blogs
    if select_cate_id and select_cate_id.isdigit():
        select_cate_id = int(select_cate_id)
        show_blog = [blog for blog in all_blogs if blog.get('category_id',0) == select_cate_id]
    for blog in show_blog:
        blog['category_name'] = cate_sln.get_category_name(blog.get('category_id',0))
    return render_template('index.html',blogs = show_blog,categories = all_categories,selected_cate = select_cate_id)

@app.route('/categories', methods=['GET', 'POST'])
def categories():
    if request.method == 'GET':
        categories = cate_sln.load_categories()
        return render_template('categories.html', categories=categories)
    else:
        category_name = request.form.get('name', '').strip()
        if not category_name:
            return redirect(url_for('categories'))
        categories = cate_sln.load_categories()
        existing = next((c for c in categories if c['name'] == category_name), None)
        if existing:
            return redirect(url_for('categories'))
        new_category = {
            'id': max([c['id'] for c in categories], default=0) + 1,
            'name': category_name
        }
        categories.append(new_category)
        cate_sln.save_categories(categories)
        return redirect(url_for('categories'))

@app.route('/delete_category/<int:category_id>')
def delete_category(category_id):
    categories = cate_sln.load_categories()
    categories = [c for c in categories if c['id'] != category_id]
    cate_sln.save_categories(categories)
    blogs = blog_sl.load_blogs()
    for blog in blogs:
        if blog.get('category_id') == category_id:
            blog['category_id'] = None
    blog_sl.save_blogs(blogs)

    return redirect(url_for('categories'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        users = user_sl.load_users()
        new_id = max([u['id'] for u in users], default=0) + 1
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        register_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if not username or not password or not confirm_password:
            return render_template('register.html',error="值不能为空")
        if not 3 <= len(username) <= 20 or not 6 <= len(password) <= 20 or not 6 <= len(confirm_password) <= 20:
            print(len(username),len(password),len(confirm_password))
            return render_template('register.html',error="请输入正确的条件")
        if not password == confirm_password:
            return render_template('register.html',error="两次密码不一致")
        for u in users:
            if u['username'] == username:
                return render_template('register.html',error="该用户名已被注册")
        new_user = {
            "id": new_id,
            "username": username,
            "password": password,
            "register_time": register_time
        }
        users.append(new_user)
        user_sl.save_users(users)
        return redirect(url_for('index'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        username = request.form['username']
        password = request.form['password']
        users = user_sl.load_users()
        for u in users:
            if u["username"] == username:
                if u['password'] == password:
                    session['user']=username
                    session.permanent = True
                    return redirect(url_for('index'))
                else:
                    return render_template('login.html',error='密码错误!')
        return render_template('login.html',error='用户名错误！')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/add', methods=['GET', 'POST'])
def add_blog():
    if request.method == "GET":
        categorie = cate_sln.load_categories()
        return render_template("add.html",categories=categorie)
    else:
        title = request.form["title"]
        content = request.form["content"]
        category_id = request.form.get("category_id")
        cover_filename = None
        if 'cover' in request.files:
            file = request.files['cover']
            if file and file.filename != '' and upload.allowed_file(file.filename):
                filename = secure_filename(file.filename)
                timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
                cover_filename = f"{timestamp}_{filename}"
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], cover_filename))
        blogs = blog_sl.load_blogs()
        new_id = max([blog['id'] for blog in blogs], default=0) + 1
        new_time = datetime.now().strftime("%Y-%m-%d-%H")
        new_blog = {
            "id": new_id,
            "title": title,
            "content": content,
            'cover': cover_filename,
            'category_id': int(category_id),
            'author': session['user'],
            "create_time": new_time
        }
        blogs.append(new_blog)
        blog_sl.save_blogs(blogs)
        return redirect(url_for("index"))

@app.route('/blog/<int:blog_id>')
def blog_detail(blog_id):
    blogs = blog_sl.load_blogs()
    for i in blogs:
        if i["id"] == blog_id:
            return render_template('detail.html',blog=i)
    return "博客不存在",404

@app.route('/edit/<int:blog_id>', methods=['GET', 'POST'])
def edit_blog(blog_id):
    blogs = blog_sl.load_blogs()
    blog = next((b for b in blogs if b['id'] == blog_id), None)
    if not blog:
        return "博客不存在",404
    if request.method == "GET":
        categories = cate_sln.load_categories()
        return render_template("edit.html",blog=blog,categories=categories)
    else:
        blog["title"] = request.form['title']
        blog["update_time"] = datetime.now().strftime('%Y-%m-%d %H:%M')
        blog["content"] = request.form['content']
        blog['category_id'] = int(request.form.get('category_id')) if request.form.get('category_id') else None
        if 'cover' in request.files:
            file = request.files['cover']
            if file and file.filename != '' and upload.allowed_file(file.filename):
                if blog.get('cover'):
                    old_cover_path = os.path.join(app.config['UPLOAD_FOLDER'], blog['cover'])
                    if os.path.exists(old_cover_path):
                        os.remove(old_cover_path)
                filename = secure_filename(file.filename)
                timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
                cover_filename = f"{timestamp}_{filename}"
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], cover_filename))
                blog['cover'] = cover_filename
        blog_sl.save_blogs(blogs)
        return redirect(url_for("blog_detail",blog_id=blog_id))

@app.route('/delete/<int:blog_id>')
def delete_blog(blog_id):
    blogs = blog_sl.load_blogs()
    for i in blogs:
        if i["id"] == blog_id:
            blogs.remove(i)
    blog_sl.save_blogs(blogs)
    return redirect(url_for("index",blog_id=blog_id))

if __name__ == "__main__":
    app.run(debug=True)