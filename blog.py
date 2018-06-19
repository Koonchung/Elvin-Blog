# -*- coding: utf-8 -*-
# author: Chan

from flask import Flask, render_template, g, flash, request, session, redirect, abort, url_for, Markup
from flask_bootstrap import Bootstrap
from models import db, Article, User
import markdown
import hashlib

app = Flask(__name__)
bootstrap = Bootstrap(app)
db.create_all()
app.secret_key = "your_secret_key"  # 随便输入字符串


def toMD5(password):
    return hashlib.md5(password.encode(encoding='utf-8')).hexdigest()

@app.template_filter('toMarkdown')
def toMarkdown(content):
    return Markup(markdown.markdown(content))


@app.route('/')
def show_main_page(username=None):
    rows = Article.query.all()
    return render_template('main_page.html', rows=rows)


@app.route('/login', methods=['GET', 'POST'])
def show_login_page():
    if request.method == 'GET':
        return render_template('login_page.html')
    elif request.method == 'POST':
        username = request.form['username']
        password = toMD5(request.form['password'])
        if not User.query.filter_by(username=username).all():
            flash("用户名不存在")
        elif password not in User.query.filter_by(username=username).first().password:
            flash("密码错误")
        else:
            # flash("登录成功")
            session['username'] = username
            return redirect(url_for('show_admin_page'))
    return render_template('login_page.html')


@app.route('/logout')
def show_logout_page():
    session.pop('username')
    return redirect(url_for('show_main_page'))


# @app.route('/regist', methods=['POST', 'GET'])
# def regist_page():
#     if request.method == 'GET':
#         return render_template('regist_page.html')
#     elif request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         password2 = request.form['password2']
#         if not all([username, password, password2]):
#             flash("数据不完整")
#         elif password != password2:
#             flash("密码不一致")
#         elif len(User.query.filter_by(username=request.form['username']).all()) != 0:
#             flash("该用户名已存在")
#         else:
#             data = User(username, password)
#             db.session.add(data)
#             db.session.commit()
#             # flash("注册成功")
#             return redirect(url_for('show_main_page'))
#     return redirect(url_for('regist_page'))


@app.route('/admin/writing', methods=['POST', 'GET'])
def writing_page():
    if 'username' in session:
        if request.method == 'GET':
            return render_template('writing_page.html')
        elif request.method == 'POST':
            title = request.form['title']
            content = Markup(markdown.markdown(request.form['content']))
            author = request.form['author']
            data = Article(title, content, author)
            db.session.add(data)
            db.session.commit()
            # session.pop('username')
            return redirect(url_for('show_admin_page'))
    else:
        return render_template('login_page.html')


@app.route('/admin/edit/<int:article_id>', methods=['POST', 'GET'])
def edit_page(article_id):
    if 'username' in session:
        if request.method == 'GET':
            row = Article.query.get(article_id)
            return render_template('edit_page.html', row=row)
        elif request.method == 'POST':
            title = request.form['title']
            content = Markup(markdown.markdown(request.form['content']))
            author = request.form['author']
            Article.query.filter_by(id=article_id).first().content = content
            Article.query.filter_by(id=article_id).first().author = author
            db.session.commit()
            # session.pop('username')
            return redirect(url_for('show_admin_page'))
    else:
        return render_template('login_page.html')


@app.route('/admin/delete/<int:article_id>')
def delete_page(article_id):
    if 'username' in session:
        data = Article.query.get(article_id)
        db.session.delete(data)
        db.session.commit()
        return redirect(url_for('show_admin_page'))
    else:
        return render_template('login_page.html')


@app.route('/admin/manage')
def manage_page():
    return render_template('admin_page.html')


@app.route('/admin')
def show_admin_page():
    if 'username' in session:
        rows = Article.query.all()
        return render_template('admin_page.html', rows=rows)
    else:
        return render_template('login_page.html')


@app.route('/article/<int:article_id>')
def show_content_page(article_id):
    row = Article.query.get(article_id)
    return render_template('content_page.html', row=row, article_id=article_id)


@app.route('/about')
def show_about_page():
    return render_template('about_page.html')


# @app.route('/contact')
# def show_contact_page():
#     return render_template('contact_page.html')


if __name__ == '__main__':
    # app.run(debug=True)
    app.run(host='0.0.0.0', port='5001')
