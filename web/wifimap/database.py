# This file really needs a better name. We'll discuss later
from wifimap import db, config
import sqlalchemy
from flask.ext.sqlalchemy import SQLAlchemy
from collections import defaultdict
from sqlalchemy.sql.expression import asc
from datetime import datetime

"""
Tables:
    Checkins:
        phone UUID - foreign key
        datetime
        GPS location
        AP - foreign key
        signal
        performance

    AP:
        bssid
        ssid

    Phones:
        phone_id
        checkins
        latest_checkin
"""

class Checkin(db.Model):
    __tablename__ = 'checkin'
    phone_id = db.Column(db.String(100), db.ForeignKey('phone.id'), primary_key=True)
    datetime = db.Column(db.String(50), primary_key=True)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    ap_bssid = db.Column(db.String(12), db.ForeignKey('ap.bssid'), primary_key=True)
    ssid = db.Column(db.String(50), db.ForeignKey('network.ssid'), primary_key=True)
    signal = db.Column(db.Integer)
    performance = db.Column(db.Integer)

    def __repr__(self):
        return '<Checkin %s, %s, %s, %s, %s, %s, %s>' % \
                ( str(self.phone_id), str(self.datetime), \
                  str(self.latitude), str(self.longitude),\
                  str(self.ap_bssid), str(self.ssid), str(self.signal) )

class AP(db.Model):
    __tablename__ = 'ap'
    bssid = db.Column(db.String(12), primary_key=True)
    _ssid = db.Column(db.String(50), db.ForeignKey('network.ssid'), name='ssid', primary_key=True)

    checkins = db.relationship('Checkin', backref='ap')

    def __init__(self, bssid, ssid):
        db.Model.__init__(self)
        self.bssid = bssid
        self.ssid = ssid

    @property
    def ssid(self):
        return self._ssid

    @ssid.setter
    def ssid(self, value):
        self._ssid = str(value)[:20]

    def __repr__(self):
        return '<AP %s, %s>' % (str(self.bssid), str(self._ssid))

class Network(db.Model):
    __tablename__ = 'network'
    _ssid = db.Column(db.String(50), name='ssid', primary_key=True)
    
    APs = db.relationship('AP', backref='network')
    checkins = db.relationship('Checkin', backref='network')
    
    def __init__(self, ssid):
        db.Model.__init__(self)
        self.ssid = ssid

    @property
    def ssid(self):
        return self._ssid

    @ssid.setter
    def ssid(self, value):
        self._ssid = str(value)[:50]

    def __repr__(self):
        return '<Network %s>' % str(self._ssid) 

class Phone(db.Model):
    __tablename__ = 'phone'
    id = db.Column(db.String(36), primary_key=True)
    #checkins = db.relationship('Checkin', backref='phone', primaryjoin='id==Checkin.phone_id')
    checkins = db.relationship('Checkin', backref='phone')

    @property
    def last_checkin(self):
        return Checkin.query.filter_by(phone_id=self.id).order_by(Checkin.datetime).first()

