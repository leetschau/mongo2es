import requests
import json
import sys
import re

cmdFmt = 'python3 ' + sys.argv[0] + ' <input-file> <index-name> <type-name>'
example = 'python3 uploadES.py fairs.json production Fair'
if len(sys.argv) != 4:
    print('Bad format, upload cancelled.')
    print('Format:\n%s\nExample:\n%s' % (cmdFmt, example))
    sys.exit(1)

inp = sys.argv[1]
baseUrl = 'http://192.168.100.24:9200/%s/%s/' % (sys.argv[2], sys.argv[3])


def conv_date(afair: str) -> str:
    DEFAULT_DATE = '"2011-11-11T00:00:00.000Z"'
    trans_normal = re.sub(
            r'{"\$date":("2\d\d\d-\d\d-\d\dT\d\d:\d\d:\d\d.\d\d\dZ")}',
            r'\1',
            afair)
    # 不符合标准格式的日期全部强制转换为默认日期
    return re.sub(r'{"\$date":(".*?")}', DEFAULT_DATE, trans_normal)

with open(inp) as f:
    cnt = 0
    for line in f:
        fair = json.loads(conv_date(line.strip()))
        for rec in fair['recurrence']:
            recId = rec['_id']
            cnt = cnt + 1
            print('up no.%d: %s ...' % (cnt, recId))
            targetUrl = baseUrl + recId
            del rec['_id']
            res = requests.post(targetUrl, data=json.dumps(rec)).json()
            if 'status' in res:
                print('upload error for %s: %s' % (recId, res['error']),
                      file=sys.stderr)
