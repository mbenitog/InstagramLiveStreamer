import json, time, random, base64, hmac, hashlib, datetime, urllib.request


def microtime(get_as_float=False):
    d = datetime.now()
    t = time.mktime(d.timetuple())
    if get_as_float:
        return t
    else:
        ms = d.microsecond / 1000000.
        return '%f %d' % (ms, t)


def getUserId(username):
    resp = urllib.request.urlopen("http://instagram.com/{}/".format(username))
    resp = resp.read().decode()
    resp = resp.split(',"id":"')[1]
    resp = resp.split('"')[0]
    return resp


def createBroadcast(api, RESOLUTION):
    data = json.dumps({'_uuid': api.uuid,
                           '_uid': api.username_id,
                           'preview_height': RESOLUTION[1],
                           'preview_width': RESOLUTION[0],
                           'broadcast_message': '',
                           'broadcast_type': 'RTMP',
                           'internal_only': 0,
                           '_csrftoken': api.token})
    return api.SendRequest('live/create/', api.generateSignature(data))


def startBroadcast(api, broadcastId, send_notifications):
    data = json.dumps({'_uuid': api.uuid,
                           '_uid': api.username_id,
                           'should_send_notifications': int(send_notifications),
                           '_csrftoken': api.token})
    return api.SendRequest('live/' + str(broadcastId) + '/start', api.generateSignature(data))


def stopBroadcast(api, broadcastId):
        data = json.dumps({'_uuid': api.uuid,
                           '_uid': api.username_id,
                           '_csrftoken': api.token})
        return api.SendRequest('live/' + str(broadcastId) + '/end_broadcast/', api.generateSignature(data))


def addBroadcastToLive(api, broadcastId):
        data = json.dumps({'_uuid': api.uuid,
                           '_uid': api.username_id,
                           '_csrftoken': api.token})
        return api.SendRequest('live/' + str(broadcastId) + '/add_to_post_live/', api.generateSignature(data))


def addBroadcastToFeed(api,broadcastId):
    data = json.dumps({ '_uuid': api.uuid,
                            '_uid': api.username_id,
                            '_csrftoken': api.token})
    return api.SendRequest('live/' + str(broadcastId) + '/add_to_post_live/', api.generateSignature(data))


def UserBreadcrumb(length):
    key = 'iN4$aGr0m'
    date = microtime(True)*1000
    term = random.randrange(2,3)*1000 + length * random.randrange(15,20) * 100
    text_change_event_count = round(length/random.randrange(2,3))
    if text_change_event_count==0:
        text_change_event_count=1
    data = str(length)+" "+str(term)+" "+str(text_change_event_count)+" "+str(date)
    return base64.standard_b64encode(hmac.new(key.encode(),data.encode(),hashlib.sha256).digest())+b"\n"+base64.standard_b64encode(data.encode())+b"\n"


def generateUUID(dashes=True):
    if dashes:
        return "1c9bd518-002e-421b-8d38-5705a95c5a05"
    else:
        return "1c9bd518-002e-421b-8d38-5705a95c5a05".replace("-","")
