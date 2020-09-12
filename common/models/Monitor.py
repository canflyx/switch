# coding: utf-8
from sqlalchemy import Boolean, Column, DateTime, Integer, Text
from application import db


class Monitor(db.Model):
    __tablename__ = 'Monitor'

    id = db.Column(db.Integer, primary_key=True)
    ipaddr = db.Column(db.Text)
    sw = db.Column(db.Text)
    port = db.Column(db.Text)
    create_time = db.Column(db.Text)
    update_time = db.Column(db.Text)
    isok = db.Column(db.Integer)
