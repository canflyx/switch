# coding: utf-8
from sqlalchemy import Column, DateTime, Integer, Text
from application import db



class ARP(db.Model):
    __tablename__ = 'ARP'

    id = db.Column(db.Integer, primary_key=True)
    ipaddr = db.Column(db.Text)
    macadd = db.Column(db.Text)
    update_time = db.Column(db.Text)
    swip = db.Column(db.Text)
    note = db.Column(db.Text)
