import datetime

from flask import (Blueprint, current_app, flash, g, render_template, request, session)

from wow import db
from wow.auth import login_required
from wow.gameserver import check_status
from wow.models.characters import Characters
from wow.models.realmd import Account, AccountLogon

bp = Blueprint("index", __name__)

races = ["种族", "人类", "兽人", "矮人", "暗夜精灵", "亡灵", "牛头人", "侏儒", "巨魔"]
classes = ["职业", "战士", "圣骑士", "猎人", "潜行者", "牧师", "死亡骑士", 
    "萨满", "法师", "术士", "武僧", "德鲁伊", "恶魔猎手", "唤魔师"]
genders = ["男性", "女性"]


@bp.route("/")
def index():
    status = check_status()
    count = 0
    if status["db"]:
        count = Characters.query.filter_by(online=1).count()
    status["count"] = count
    status["ver"] = current_app.config["SERVER_VER"]
    status["client"] = current_app.config["SERVER_CLIENT_URL"]
    status["logon"] = current_app.config["SERVER_LOGON_URL"]

    nav = {"index": True}
    return render_template("index.html", status=status, nav=nav)


@bp.route("/test")
def test():
    return render_template("wow.html")


@bp.route("/top", defaults={"tp": "level", "qty": 50})
@bp.route("/top/<tp>", defaults={"qty": 50})
@bp.route("/top/<tp>/<int:qty>")
def top(tp, qty=50):
    tps = {"level": "等级", "money": "财富", "totaltime": "时长"}

    error = None
    status = check_status()
    if not status["db"]:
        error = "数据库未开启"
    result = []
    if tp not in tps:
        error = "Unkown link."
    if qty > 50 and not session.get("admin", False):
        error = "Max to show 50 records."
    if error is None:
        chs = db.session.query(
            Characters.guid,
            Characters.account,
            Characters.name,
            Characters.race,
            Characters.class_,
            Characters.gender,
            Characters.online,
            Characters.totaltime,
            Characters.level,
            Characters.money,
        )
        if tp == "level":
            chs = chs.order_by(Characters.level.desc(), Characters.money.desc()).limit(
                qty
            )
        if tp == "money":
            chs = chs.order_by(Characters.money.desc(), Characters.level.desc()).limit(
                qty
            )
        if tp == "totaltime":
            chs = chs.order_by(
                Characters.totaltime.desc(), Characters.level.desc()
            ).limit(qty)
        # 查询机器人账号
        ras = Account.query.filter(Account.username.like("RNDBOT%")).all()
        ra_ids = [ra.id for ra in ras]
        for ch in chs:
            result.append(
                {
                    "name": ch.name,
                    "type": "robot.png" if ch.account in ra_ids else "player.png",
                    "type_alt": "机器人" if ch.account in ra_ids else "玩家",
                    "race": f"{ch.race}-{ch.gender}",
                    "race_alt": races[ch.race] + genders[ch.gender],
                    "class": ch.class_,
                    "class_alt": classes[ch.class_],
                    "online": "on" if ch.online else "off",
                    "online_alt": "在线" if ch.online else "离线",
                    "totaltime": ch.totaltime,
                    "level": ch.level,
                    "money": ch.money,
                }
            )

    if error:
        flash(error)

    nav = {"top": True}
    return render_template("top.html", result=result, tp=tps[tp], nav=nav)


@bp.route("/account_info", methods=("GET", "POST"))
@login_required
def account_info():
    logon = (
        db.session.query(db.func.max(AccountLogon.loginTime))
        .filter(AccountLogon.accountId == g.user.id)
        .scalar()
    )
    if logon is None:
        logon = ""
    chs = Characters.query.filter_by(account=g.user.id).all()
    result = []
    for ch in chs:
        result.append(
            {
                "name": ch.name,
                "race": f"{ch.race}-{ch.gender}",
                "race_alt": races[ch.race] + genders[ch.gender],
                "class": ch.class_,
                "class_alt": classes[ch.class_],
                "online": "on" if ch.online else "off",
                "online_alt": "在线" if ch.online else "离线",
                "totaltime": ch.totaltime,
                "level": ch.level,
                "money": ch.money,
                "logout_time": datetime.datetime.fromtimestamp(ch.logout_time).strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
            }
        )

    nav = {"auth": True}
    return render_template(
        "auth/account_info.html", result=result, nav=nav, logon=logon
    )
