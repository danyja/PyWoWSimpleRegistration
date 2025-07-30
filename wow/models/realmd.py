from wow import db
from datetime import datetime


class Account(db.Model):
    __tablename__ = "account"
    __bind_key__ = "realmd"
    id = db.Column(db.Integer, primary_key=True, nullable=False, comment="Identifier")
    username = db.Column(db.String(32), unique=True, nullable=False, default="")
    gmlevel = db.Column(db.SmallInteger, nullable=False, default=0)
    sessionkey = db.Column(db.Text)
    v = db.Column(db.Text)
    s = db.Column(db.Text)
    email = db.Column(db.Text)
    joindate = db.Column(
        db.DateTime, nullable=False, default=datetime.now()
    )
    lockedIp = db.Column(db.String(30), nullable=False, default="0.0.0.0")
    failed_logins = db.Column(db.Integer, nullable=False, default=0)
    locked = db.Column(db.SmallInteger, nullable=False, default=0)
    last_module = db.Column(db.String(32), default="")
    module_day = db.Column(db.Integer, nullable=False, default=0)
    active_realm_id = db.Column(db.Integer, nullable=False, default=0)
    expansion = db.Column(db.SmallInteger, nullable=False, default=0)
    mutetime = db.Column(db.BigInteger, nullable=False, default=0)
    locale = db.Column(db.String(4), nullable=False, default="")
    os = db.Column(db.String(4), nullable=False, default="0")
    platform = db.Column(db.String(4), nullable=False, default="0")
    token = db.Column(db.Text)
    flags = db.Column(db.Integer, nullable=False, default=0)

    def __repr__(self):
        return f"<Account {self.username}>"


class AccountBanned(db.Model):
    __tablename__ = "account_banned"
    __bind_key__ = "realmd"
    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, nullable=False, default=0, comment="Account id")
    banned_at = db.Column(db.BigInteger, nullable=False, default=0)
    expires_at = db.Column(db.BigInteger, nullable=False, default=0)
    banned_by = db.Column(db.String(50), nullable=False)
    unbanned_at = db.Column(db.BigInteger, nullable=False, default=0)
    unbanned_by = db.Column(db.String(50))
    reason = db.Column(db.String(255), nullable=False)
    active = db.Column(db.SmallInteger, nullable=False, default=1)

    def __repr__(self):
        return f"<AccountBanned account_id={self.account_id} active={self.active}>"


class AccountLogon(db.Model):
    __tablename__ = "account_logons"
    __bind_key__ = "realmd"
    id = db.Column(db.Integer, primary_key=True)
    accountId = db.Column(db.Integer, db.ForeignKey("account.id"), nullable=False)
    ip = db.Column(db.String(30), nullable=False)
    loginTime = db.Column(db.TIMESTAMP, nullable=False, default=datetime.now())
    loginSource = db.Column(db.Integer, nullable=False, default=0)

    # 如果需要建立关系
    # account = db.relationship('Account', backref='logons', foreign_keys=[accountId])

    def __repr__(self):
        return f"<AccountLogon accountId={self.accountId} ip={self.ip} loginTime={self.loginTime}>"


class IPBanned(db.Model):
    __tablename__ = "ip_banned"
    __table_args__ = {"comment": "Banned IPs"}
    __bind_key__ = "realmd"
    ip = db.Column(db.String(32), primary_key=True, nullable=False, default="0.0.0.0")
    banned_at = db.Column(db.BigInteger, nullable=False)
    expires_at = db.Column(db.BigInteger, nullable=False)
    banned_by = db.Column(db.String(50), nullable=False, default="[Console]")
    reason = db.Column(db.String(255), nullable=False, default="no reason")

    def __repr__(self):
        return f"<IPBanned ip={self.ip} expires_at={self.expires_at}>"


class RealmCharacters(db.Model):
    __tablename__ = "realmcharacters"
    __table_args__ = (
        db.PrimaryKeyConstraint("realmid", "acctid"),  # 复合主键
        {"comment": "Realm Character Tracker"},
    )
    __bind_key__ = "realmd"
    realmid = db.Column(
        db.Integer, db.ForeignKey("realmlist.id"), nullable=False, default=0
    )  # 关联到realm表
    acctid = db.Column(
        db.BigInteger, db.ForeignKey("account.id"), nullable=False
    )  # 关联到account表
    numchars = db.Column(db.SmallInteger, nullable=False, default=0)

    # 关系定义
    # realm = db.relationship('RealmList', backref='characters')
    # account = db.relationship('Account', backref='realm_stats')

    def __repr__(self):
        return f"<RealmCharacters realm={self.realmid} account={self.acctid} chars={self.numchars}>"


class RealmList(db.Model):
    __tablename__ = "realmlist"
    __table_args__ = {"comment": "Realm System"}
    __bind_key__ = "realmd"
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(32), nullable=False, default="")
    address = db.Column(db.String(32), nullable=False, default="127.0.0.1")
    port = db.Column(db.Integer, nullable=False, default=8085)
    icon = db.Column(db.SmallInteger, nullable=False, default=0)
    realmflags = db.Column(
        db.SmallInteger,
        nullable=False,
        default=2,
        comment="Supported masks: 0x1 (invalid, not show in realm list), 0x2 (offline, set by mangosd), 0x4 (show version and build), 0x20 (new players), 0x40 (recommended)",
    )
    timezone = db.Column(db.SmallInteger, nullable=False, default=0)
    allowedSecurityLevel = db.Column(db.SmallInteger, nullable=False, default=0)
    population = db.Column(db.Float, nullable=False, default=0.0)
    realmbuilds = db.Column(db.String(64), nullable=False, default="")

    # 与realmcharacters表的一对多关系
    # characters = db.relationship('RealmCharacters', back_populates='realm')

    def __repr__(self):
        return f"<RealmList {self.id}: {self.name} ({self.address}:{self.port})>"


class SystemFingerprintUsage(db.Model):
    __tablename__ = "system_fingerprint_usage"
    __bind_key__ = "realmd"
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    fingerprint = db.Column(db.Integer, nullable=False)
    account = db.Column(db.Integer, db.ForeignKey("account.id"), nullable=False)
    ip = db.Column(db.String(16), nullable=False)
    realm = db.Column(db.Integer, db.ForeignKey("realmlist.id"), nullable=False)
    time = db.Column(db.DateTime)
    architecture = db.Column(db.String(16))
    cputype = db.Column(db.String(64))
    activecpus = db.Column(db.Integer)
    totalcpus = db.Column(db.Integer)
    pagesize = db.Column(db.Integer)

    # 关系定义
    # account_rel = db.relationship('Account', backref='fingerprints')
    # realm_rel = db.relationship('RealmList', backref='fingerprint_usages')

    def __repr__(self):
        return f"<SystemFingerprintUsage fingerprint={self.fingerprint} account={self.account} ip={self.ip}>"


class Uptime(db.Model):
    __tablename__ = "uptime"
    __table_args__ = (
        db.PrimaryKeyConstraint("realmid", "starttime"),  # 复合主键
        {"comment": "Uptime system"},
    )
    __bind_key__ = "realmd"
    realmid = db.Column(db.Integer, db.ForeignKey("realmlist.id"), nullable=False)
    starttime = db.Column(db.Integer, nullable=False, default=0)
    startstring = db.Column(db.String(64), nullable=False, default="")
    uptime = db.Column(db.Integer, nullable=False, default=0)
    maxplayers = db.Column(db.Integer, nullable=False, default=0)

    # 与realmlist的关系
    # realm = db.relationship('RealmList', backref=db.backref('uptimes', lazy='dynamic'))

    def __repr__(self):
        return (
            f"<Uptime realm={self.realmid} "
            f"uptime='{self.pretty_uptime()}' "
            f"maxplayers={self.maxplayers}>"
        )

    def pretty_uptime(self):
        """将秒数转换为可读的时间格式"""
        minutes, seconds = divmod(self.uptime, 60)
        hours, minutes = divmod(minutes, 60)
        days, hours = divmod(hours, 24)
        return f"{days}d {hours}h {minutes}m {seconds}s"
