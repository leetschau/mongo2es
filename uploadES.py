import requests
import json
import sys

cmdFmt = 'python3 ' + sys.argv[0] +\
            ' <input-file> <output-file> <index-name> <type-name>'
example = 'python3 uploadES.py fairs.json production Fair'
if len(sys.argv) != 4:
    print('Bad format, upload cancelled.')
    print('Format:\n%s\nExample:\n%s' % (cmdFmt, example))
    sys.exit(1)

inp = sys.argv[1]
baseUrl = 'http://192.168.100.24:9200/%s/%s/' % (sys.argv[2], sys.argv[3])

def dateObj(date) -> str:
    DEFAULT_DATE = '2011-11-11T00:00:00.000Z'
    if isinstance(date, dict) and '$date' in date:
        return date['$date']
    if isinstance(date, str):
        return date
    return DEFAULT_DATE

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
        if 'recurrence' in obj:
            for rec in obj['recurrence']:
                if 'timeStart' in rec:
                    rec['timeStart'] = dateObj(rec['timeStart'])
                if 'timeEnd' in rec:
                    rec['timeEnd'] = dateObj(rec['timeEnd'])
        if 'logo' in obj:
            for logo in obj['logo']:
                if 'createdAt' in logo:
                    logo['createdAt'] = dateObj(logo['createdAt'])
        res = requests.post(targetUrl, data = json.dumps(obj)).json()
        if 'status' in res:
            print('upload error for %s: %s' % (objId, res['error']),
                    file=sys.stderr)
