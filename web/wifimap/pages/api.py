from wifimap import app, db, database
from wifimap.database import Checkin, AP, Phone, Network
from flask import request, jsonify, json, make_response

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
    #print entries
    for e in entries:
        print e
        if verify_entry(e):
            db.session.add(Checkin(
                    phone_id=e['phone_id'], datetime=e['datetime'],
                    latitude=e['latitude'], longitude=e['longitude'],
                    ap_bssid=e['bssid'], signal=e['signal'], 
                    performance=e['performance']))

            if AP.query.filter_by(bssid=e['bssid']) is not None:
                db.session.add(AP(bssid=e['bssid'], ssid=e['ssid']))
            
            if Network.query.filter_by(_ssid=e['ssid']) is not None:
                db.session.add(Network(ssid=e['ssid']))
            
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

@app.route('/api/render/', methods=['GET', 'POST'])
def api_send_render():
    print request.form.get('json', None)
    target_time = json.loads(request.form.get('json', None))['datetime']
    ssid= json.loads(request.form.get('json', None))['ssid']
    #target_time = request.json['datetime']
    #ssid = request.json['datetime']
    entries = []
    for c in get_checkins_near_time(target_time, 10, ssid):
        entries.append({'latitude' : c.latitude, 'longitude' : c.longitude,
                        'ssid' : c.ssid,'signal_strength' : c.signal, 
                        'performance' : c.performance})
    #return jsonify(entries)
    print json.dumps(entries)
    return make_response(json.dumps(entries))

