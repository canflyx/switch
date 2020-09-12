# coding: utf-8
from sqlalchemy import Column, DateTime, Integer, Text
from application import db


class MAC(db.Model):
    __tablename__ = 'MAC'

    id = db.Column(db.Integer, primary_key=True)
    macadd = db.Column(db.Text)
    port = db.Column(db.Text)
    swip = db.Column(db.Integer)
    update_time = db.Column(db.Text)
    note = db.Column(db.Text)
