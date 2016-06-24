#!/usr/bin/env python
import datetime
from sqlalchemy import Integer, String, Boolean, DateTime
from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

R_User_SSHUser = Table("bl_r_user_sshuser", Base.metadata,
                       Column('id', Integer, autoincrement=True, primary_key=True),
                       Column('uid', Integer, ForeignKey('bl_login_user.id'), primary_key=True),
                       Column('sid', Integer, ForeignKey('bl_ssh_user.id'), primary_key=True)
                       )

R_User_Group = Table("bl_r_user_group", Base.metadata,
                     Column('id', Integer, autoincrement=True, primary_key=True),
                     Column('uid', Integer, ForeignKey('bl_login_user.id'), primary_key=True),
                     Column('gid', Integer, ForeignKey('bl_groups.id'), primary_key=True)
                     )

R_Host_Group = Table("bl_r_host_group", Base.metadata,
                     Column('id', Integer, autoincrement=True, primary_key=True),
                     Column('hid', Integer, ForeignKey('bl_hosts.id'), primary_key=True),
                     Column('gid', Integer, ForeignKey('bl_groups.id'), primary_key=True)
                     )


class SSH_User(Base):
    __tablename__ = 'bl_ssh_user'
    id = Column(Integer, autoincrement=True, primary_key=True)
    hid = Column(Integer, ForeignKey('bl_hosts.id'), primary_key=True)
    auth_type = Column(Integer, default=1)
    auth_user = Column(String(50), primary_key=True)
    auth_key = Column(String(50), nullable=False)

    def __init__(self, auth_user, auth_key, auth_type):
        self.auth_user = auth_user
        self.auth_type = auth_type
        self.auth_key = auth_key


class Login_User(Base):
    __tablename__ = 'bl_login_user'
    id = Column(Integer, autoincrement=True, primary_key=True)
    username = Column(String(50), unique=True)
    password = Column(String(50), nullable=False)
    name = Column(String(30))
    role = Column(String(10), nullable=False, default='user')
    isdel = Column(Boolean, default=False)
    expired = Column(DateTime)
    groups = relationship('Groups', secondary=R_User_Group, backref="userlist")
    sshusers = relationship('SSH_User', secondary=R_User_SSHUser, backref="sshuserlist")
    oplog = relationship('Op_Logs', backref='userlist')

    def __init__(self, username, name, role, isdel, expired, password):
        self.username = username
        self.name = name
        self.role = role
        self.isdel = isdel
        self.expired = expired
        self.password = password

    def __repr__(self):
        return "Login_user(id={id},username={username},name={name},role={role}，isdel={isdel},expired={expired})".format(
            id=self.id,
            username=self.username,
            name=self.name,
            role=self.role,
            isdel=self.isdel,
            expired=self.expired
        )


class Groups(Base):
    __tablename__ = 'bl_groups'
    id = Column(Integer, autoincrement=True, primary_key=True)
    groupname = Column(String(50), primary_key=True)

    def __init__(self, groupname):
        self.groupname = groupname

    def __repr__(self):
        return "Groups(id={id},groupname={groupname})".format(id=self.id,
                                                             groupname=self.groupname)


class Hosts(Base):
    __tablename__ = 'bl_hosts'
    id = Column(Integer, autoincrement=True, primary_key=True)
    hostname = Column(String(50), nullable=False)
    ipaddr = Column(String(15), primary_key=True)
    sshport = Column(Integer, default=22, nullable=False)
    sshuser = relationship("SSH_User", backref="hostslist")
    groups = relationship("Groups",
                          secondary=R_Host_Group,
                          backref="hostlist")

    def __init__(self, hostname, ipaddr, sshport):
        self.hostname = hostname
        self.ipaddr = ipaddr
        self.sshport = sshport


class Op_Logs(Base):
    __tablename__ = 'bl_op_logs'
    id = Column(Integer, autoincrement=True, primary_key=True)
    uid = Column(Integer, ForeignKey('bl_login_user.id'))
    opdate = Column(DateTime, nullable=False)
    optype = Column(String(50), nullable=False)
    opmsg = Column(String(500))
