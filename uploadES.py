import requests
import json
import sys

cmdFmt = 'python3 ' + sys.argv[0] +\
            ' <input-file> <output-file> <index-name> <type-name>'
example = 'python3 uploadES.py fairs.json production Fair'
if len(sys.argv) != 4:
    print('Bad format, upload cancelled.')
    print('Format:\n%s\nExample:\n%s' % (cmdFmt, example))

inp = sys.argv[1]
baseUrl = 'http://192.168.100.24:9200/%s/%s/' % (sys.argv[2], sys.argv[3])

def dateObj(date):
    if isinstance(date, dict) and '$date' in date:
        return date['$date']
    if isinstance(date, str):
    # for Python 2.x, use `isinstance(date, basestring)`
        return date
    defaultDate =  '1970-01-01T00:00:00.000Z'
    print('Invalid data format: %s, use %s instead.' % (date, defaultDate),
            file=sys.stderr)
    return defaultDate

with open(inp) as f:
    cnt = 0
    for line in f:
        obj = json.loads(line)
        objId = obj['_id']
        cnt = cnt + 1
        print('uploading No. %d: %s ...' % (cnt, objId))
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
        if 'status' in res:
            print('upload error: %s:' % objId, file=sys.stderr)
            print(res['error'], file=sys.stderr)
