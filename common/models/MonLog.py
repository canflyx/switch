# coding: utf-8
from sqlalchemy import Column, DateTime, Integer, LargeBinary, Text
from application import db



class MonLog(db.Model):
    __tablename__ = 'MonLog'

    id = db.Column(db.Integer, primary_key=True)
    mon_id = db.Column(db.Integer)
    update_time = db.Column(db.Text)
