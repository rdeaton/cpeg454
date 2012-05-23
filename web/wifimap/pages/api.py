from wifimap import app, db, database
from wifimap.database import Checkin, AP, Phone, Network
from flask import request, jsonify, json, make_response
from datetime import datetime, date, time, timedelta
from sqlalchemy import and_

"""
checkin format
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
    entries = json.loads(request.form.get('json', None))
    failed = 0
    for e in entries:
        if verify_entry(e):
            c = Checkin(
                    phone_id=e['phone_id'], datetime=e['datetime'],
                    latitude=e['latitude'], longitude=e['longitude'],
                    ap_bssid=e['bssid'], ssid=e['ssid'], signal=e['signal'], 
                    performance=e['performance'])
            print c
            db.session.add(c)

            if AP.query.filter_by(bssid=e['bssid']).all() is None:
                db.session.add(AP(bssid=e['bssid'], ssid=e['ssid']))
                db.session.commit()
            
            if Network.query.filter_by(_ssid=e['ssid']).all() is None:
                db.session.add(Network(ssid=e['ssid']))
                db.session.commit()
            
            if Phone.query.filter_by(id=e['phone_id']).all() is None:
                db.session.add(Phone(id=e['phone_id']))
                db.session.commit()
        else:
            failed += 1
    db.session.commit()
    
    if failed != len(entries):
        return jsonify(success='True', failues=failed)
    else:
        return jsonify(success='False', failues=failed)

# DEPRECATED!
#def get_checkins_near_time(dt_value, ssid, mins=15):
#    """
#    returns checkins within 'mins' minutes of datetime
#    for a specific ssid or all SSIDs in case ssid = 'all'
#    """
#    before = dt_value - timedelta(minutes=mins)
#    after = dt_value + timedelta(minutes=mins)
#    if ssid == 'all':
#        #return Checkin.query.all()
#        return Checkin.query.\
#                filter(and_(Checkin.datetime>=before, Checkin.datetime<=after)).all()
#    else:
#        # TODO: currently, return all checkins for debug purposes
#        return Checkin.query.\
#                filter(and_(Checkin.datetime>=before, Checkin.datetime<=after)).\
#                filter(Checkin.ssid.like(ssid)).all()
#
#@app.route('/api/render/', methods=['GET', 'POST'])
#def api_send_render():
#    target_time = datetime.strptime(json.loads(request.form.get('json', None))['datetime'][:18], "%Y-%m-%dT%H:%M:%S")
#    ssid= json.loads(request.form.get('json', None))['ssid']
#    entries = []
#    for c in get_checkins_near_time(target_time, ssid, mins=15):
#        entries.append({'latitude' : c.latitude, 'longitude' : c.longitude,
#                        'ssid' : c.ssid,'signal_strength' : c.signal, 
#                        'performance' : c.performance})
#    #return jsonify(entries)
#    return make_response(json.dumps(entries))
#
