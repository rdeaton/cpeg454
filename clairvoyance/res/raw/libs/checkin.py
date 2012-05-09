import requests
from datetime import datetime
import common
import json
"""
checkin format - a list of:
{
    'phone_id' : <phone uuid or whatever>,
    'datetime' : <checkin date/time as datetime.datetime.isoformat()>,
    'latitude' : <checkin lat>,
    'longitude' : <checkin long>,
    'ssid' : <ssid of network>,
    'bssid' : <bssid of AP, 12 chars max, no colons>,
    'signal' : <signal strength, integer>,
    'performance' : <whatever performance metric we use, integer>
}

rendering format - a list of:
{
    'latitude' : <checkin lat, float>,
    'longitude' : <checkin long, float>,
    'ssid' : <network ssid, string>
    'signal' : <signal strength, integer>,
    'performance' : <whatever performance metric we use, integer>
}
"""

__all__ = ['create_checkin', 'send_checkins', 'get_render_data']

def create_checkin(phone_id=None, datetime=datetime.now().isoformat(), 
        latitude=None, longitude=None, bssid=None, ssid=None,
        signal=None, performance=None):

    return dict(phone_id=phone_id, datetime=datetime, \
                   latitude=latitude, longitude=longitude, \
                   bssid=bssid, ssid=ssid, signal=signal, \
                   performance=performance)


def send_checkins(checkins_list):
    url = 'http://%s/api/checkin/' % common.server
    payload = {}
    payload['json'] = json.dumps(checkins_list)
    r = requests.post(url, data=payload)

def get_render_data(ssid='all', datetime=datetime.now().isoformat()):
    url = 'http://%s/api/render/' % common.server
    payload = {}
    payload['json'] = json.dumps({'ssid':ssid, 'datetime':datetime})
    get = requests.post(url, data=payload)
    return get.json

if __name__ == '__main__':
    def test_post():
        c = create_checkin(phone_id='1', latitude=0, longitude=0, bssid='01234567891011', ssid='test', signal=10, performance=100)
        print c
        send_checkins([c])
    
    def test_render():
        data = get_render_data()
        print data[0]

