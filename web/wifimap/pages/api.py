from wifimap import app, db, database
from wifimap.database import Checkin, AP, Phone
from flask import request, jsonify, json

"""
checkin format
{
    'phone_id' : <phone uuid or whatever>,
    'datetime' : <checkin date/time as datetime.datetime.isoformat()>,
    'latitude' : <checkin lat>,
    'longitude' : <checkin long>,
    'bssid' : <bssid of AP, 12 chars max, no colons>,
    'signal' : <signal strength, integer>,
    'performance' : <whatever performance metric we use, integer>
}

rendering format
{
    'latitude' : <checkin lat, float>,
    'longitude' : <checkin long, float>,
    'ssid' : <network ssid, string>
    'signal' : <signal strength, integer>,
    'performance' : <whatever performance metric we use, integer>
}

"""

def verify_entry(checkin):
    # TODO: actually verify an entry, probably maybe
    return True

@app.route('/api/checkin/', methods=['GET', 'POST'])
def api_check_in():
    entries = request.json()
    failed = 0
    for e in entries:
        if verify_entry(e):
            db.session.add(Checkin(
                    phone_id=e['phone_id'], datetime=e['datetime'],
                    latitude=e['latitude'], longitude=e['longitude'],
                    ap_bssid=e['bssid'], signal=e['signal'], 
                    performance=e['performance']))
            if AP.query.filter_by(bssid=e['bssid']) is not None:
                db.session.add(AP(bssid=e['bssid'], ssid=e['ssid']))
            if Phone.query.filter_by(id=e['phone_id']) is not None:
                db.session.add(Phone(id=e['phone_id']))
        else:
            failed += 1
    db.session.commit()
    
    if failed != len(entries):
        return jsonify(success='True', failues=failed)
    else:
        return jsonify(success='False', failues=failed)

def get_checkins_near_time(time, mins, ssid):
    """
    returns checkins within 'mins' minutes of datetime
    for a specific ssid or all SSIDs in case ssid = 'all'
    """
    if ssid == 'all':
        return Checkin.query.all()
    else:
        # TODO: currently, return all checkins for debug purposes
        return Checkin.query.filter(Checkin.ssid.like(ssid)).all()


@app.route('/api/render/', methods=['GET'])
def api_send_render():
    target_time = request.json()['datetime']
    ssid = request.json()['datetime']
    entries = []
    for c in get_checkins_near_time(target_time, 10, ssid):
        entries.append({'latitude' : c.latitude, 'longitude' : c.longitude,
                        'ssid' : c.ssid,'signal_strength' : c.signal, 
                        'performance' : c.performance})
    return jsonify(entries)

