import functools
import re
import time

from flask import (Blueprint, current_app, flash, g, jsonify, redirect,
                   render_template, request, session, url_for)
from sqlalchemy.exc import IntegrityError

from wow import db
from wow.auth_tools import calculate_verifier, generate_salt
from wow.gameserver import check_status, close_server, open_server
from wow.models.realmd import Account
from wow.randcode import generate_captcha

bp = Blueprint('auth', __name__, url_prefix='/auth')

nav = {"auth": True}


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if session.get('user_id', False):
        return redirect(url_for("index.account_info"))
    error = None
    status = check_status()
    if not status["db"]:
        error = "数据库未开启"
    if request.method == 'POST':
        username = request.form['username'].strip().upper()  # 全部大写
        password = request.form['password']
        captcha_1 = request.form['captcha'].strip()

        if not username:
            error = '请输入用户名。'
        if re.search(r'[^A-Z0-9_]', username):
            error = '用户名只允许字母，数字和下划线。'
        if len(username) >= 6 and username[:6] == "RNDBOT":
            error = '不能以RNDBOT开头'
        elif not password:
            error = '请输入密码。'
        if not captcha_1 or captcha_1 != session.get('captcha', ''):
            error = "验证码错误。"
        if error is None:
            try:
                salt = generate_salt()
                veri = calculate_verifier(username, password, salt)
                new_user = Account(username=username, v=veri, s=salt)
                db.session.add(new_user)
                db.session.commit()
            except IntegrityError:
                error = f"用户名 {username} 已存在。"
            else:
                # 给所有在realmcharacters中无记录的用户创建, 基于所有服务器的账号个数(初始化为0).
                # 在旧服务器有账号的情况,不会给新服务器再添加了.
                rc_engine = db.get_engine(current_app, bind='realmd')
                with rc_engine.connect() as conn:
                    conn.execute(db.text(
                        "INSERT INTO realmcharacters (realmid, acctid, numchars) SELECT realmlist.id, account.id, 0 FROM realmlist,account LEFT JOIN realmcharacters ON acctid=account.id WHERE acctid IS NULL"))
                    conn.commit()
                return redirect(url_for("auth.login"))
    if error:
        flash(error)

    return render_template('auth/register.html', nav=nav)


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if session.get('user_id', False):
        return redirect(url_for("index.account_info"))
    error = None
    status = check_status()
    if not status["db"]:
        error = "数据库未开启"
    if request.method == 'POST':
        username = request.form['username'].strip().upper()  # 全部大写
        password = request.form['password']
        captcha_1 = request.form['captcha'].strip()
        if not username:
            error = '用户名错误。'
        if len(username) >= 6 and username[:6] == "RNDBOT":
            error = '不能以RNDBOT开头'
        if not password:
            error = '密码错误。'
        if not captcha_1 or captcha_1 != session.get('captcha', ''):
            error = "验证码错误。"

        if error is None:
            user = Account.query.filter_by(username=username).first()
            if user is None:
                error = '用户名错误。'
            elif not user.s or not user.v:
                error = '账户异常。'
            elif calculate_verifier(username, password, user.s) != user.v:
                error = '密码错误。'

        if error is None:
            session.clear()
            session['user_id'] = user.id
            return redirect(url_for('index.account_info'))
    if error:
        flash(error)

    return render_template('auth/login.html', nav=nav)


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = Account.query.filter_by(id=user_id).first()

    g.admin = session.get('admin', False)


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view


@bp.route('/change_pass', methods=('GET', 'POST'))
@login_required
def change_pass():
    error = None
    if request.method == 'POST':
        username = request.form['username'].strip().upper()  # 全部大写
        old_pass = request.form['old_password']
        new_pass = request.form['new_password']
        captcha_1 = request.form['captcha'].strip()

        if not username:
            error = "请输入用户名。"
        if len(username) >= 6 and username[:6] == "RNDBOT":
            error = '不能以RNDBOT开头'
        if not captcha_1 or captcha_1 != session.get('captcha', ''):
            error = "验证码错误。"
        if not old_pass:
            error = '请输入原密码。'
        elif calculate_verifier(g.user.username, old_pass, g.user.s) != g.user.v:
            error = '原密码错误。'
        updated = False
        if error is None and username != g.user.username:
            # 先修改用户名
            try:
                user = Account.query.filter_by(id=g.user.id).first()
                user.username = username
                db.session.commit()
                g.user = user
                updated = True
            except IntegrityError:
                db.session.rollback()
                error = f"用户 {username} 已经存在."

        if error is None:  # 修改密码，用户名变了密码必须更新
            salt = generate_salt()
            if not new_pass:
                new_pass = old_pass
            veri = calculate_verifier(g.user.username, new_pass, salt)
            user = Account.query.filter_by(id=g.user.id).first()
            user.s = salt
            user.v = veri
            db.session.commit()
            updated = True
        if error is None and updated:
            session.clear()
            return redirect(url_for('auth.login'))
    if error:
        flash(error)

    return render_template('auth/change_pass.html', username=g.user.username, nav=nav)


@bp.route('/admin', methods=('GET', 'POST'))
def admin():
    status = {}
    html_values = [["Off", "open", "打开"], ["On", "close", "关闭"]]
    if request.method == 'POST':
        error = None
        if not session.get('admin', False):
            password = request.form['password']
            captcha_1 = request.form['captcha'].strip()
            if not password or not password:
                error = '请输入密码。'
            if not captcha_1 or captcha_1 != session.get('captcha', ''):
                error = "验证码错误。"
            if error is None:
                v = calculate_verifier(
                    'admin', password, current_app.config['ADMIN_S'])
                if v != current_app.config['ADMIN_V']:
                    error = "密码错误。"
                else:
                    session['admin'] = True
                    g.admin = True
        else:
            action = request.form['action']
            if action == "change_pass":
                username = request.form['username'].strip().upper()  # 全部大写
                password = request.form['password']
                user = Account.query.filter_by(username=username).first()
                if user is None:
                    error = "用户名错误"
                else:
                    salt = generate_salt()
                    veri = calculate_verifier(username, password, salt)
                    user.s = salt
                    user.v = veri

                    db.session.commit()
            else:
                server = request.form['server']

                if server not in current_app.config['SERVERS']:
                    error = '未知服务器'
                if action not in ["open", "close"]:
                    error = '无效操作。'
                if error is None:
                    if action == "open":
                        open_server(server)
                    if action == "close":
                        close_server(server)
        if error:
            flash(error)
    if session.get('admin', False):
        results = check_status()
        for result in results:
            status[result] = html_values[int(results[result])]

    return render_template('auth/admin.html', status=status, nav=nav)


@bp.route('/admin_out')
def admin_out():
    session['admin'] = False
    g.admin = False
    return redirect(url_for('auth.admin'))


@bp.route('/captcha')
def captcha():
    last_time = session.get('captcha_time', 0)
    if time.time()-last_time < 10:
        return jsonify({'status': "请求过于频繁！请稍后再试。", 'image': ""})
    img_base64, captcha_text = generate_captcha(
        **current_app.config['CAPTCHA'])
    session['captcha'] = captcha_text
    session['captcha_time'] = time.time()
    return jsonify({'status': 'success',
                    'image': f"data:image/png;base64,{img_base64}"})
