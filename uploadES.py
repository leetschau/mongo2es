import requests
import json

inp = 'fairs.json'
baseUrl = 'http://192.168.100.24:9200/test/Fair/'

def dateObj(date):
    if isinstance(date, dict) and '$date' in date:
        return date['$date']
    if isinstance(date, basestring):
    # for Python 3.x, use `isinstance(date, str)`
        return date
    defaultDate =  '1970-01-01T00:00:00.000Z'
    print('Invalid data format: %s, use %s instead.' % (date, defaultDate))
    return defaultDate

with open(inp) as f:
    for line in f:
        obj = json.loads(line)
        objId = obj['_id']
        print('upload %s ...' % objId)
        targetUrl = baseUrl + objId
        del obj['_id']
        if 'updatedAt' in obj:
            obj['updatedAt'] = dateObj(obj['updatedAt'])
        if 'createdAt' in obj:
            obj['createdAt'] = dateObj(obj['createdAt'])
        recurrences = obj['recurrence']
        for rec in recurrences :
            if 'timeStart' in rec:
                rec['timeStart'] = dateObj(rec['timeStart'])
            if 'timeEnd' in rec:
                rec['timeEnd'] = dateObj(rec['timeEnd'])
        res = requests.post(targetUrl, data = json.dumps(obj)).json()
        print(res)
