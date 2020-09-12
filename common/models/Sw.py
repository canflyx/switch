# coding: utf-8
from sqlalchemy import Column, DateTime, Integer, LargeBinary, Text
from application import db



class Sw(db.Model):
    __tablename__ = 'Sw'

    id = db.Column(db.Integer, primary_key=True)
    ipaddr = db.Column(db.Text, nullable=False)
    user = db.Column(db.Text)
    passwd = db.Column(db.Text)
    iscore = db.Column(db.Integer)
    status=db.Column(db.Integer)
    update_time = db.Column(db.Text)
    create_time = db.Column(db.Text)
    note=db.Column(db.Text)

    @property
    def iscore_desc(self):
        iscore_mapping={
            "1":"核心",
            "0":"接入",

        }
        return iscore_mapping[str(self.iscore)]

    @property
    def status_desc(self):
        status_mapping={
            "1":"失败",
            "0":"成功",

        }
        return status_mapping[str(self.status)]