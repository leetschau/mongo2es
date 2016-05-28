import requests
import json
import sys
import re

cmdFmt = 'python3 ' + sys.argv[0] + \
         ' <input-file> <es-server-ip> <index-name> <type-name>'
example = 'python3 uploadES.py fairs.json 192.168.100.231 production Fair'
if len(sys.argv) != len(example.split(' ')) - 1:
    print('Bad format, upload cancelled.')
    print('Format:\n%s\nExample:\n%s' % (cmdFmt, example))
    sys.exit(1)

inp = sys.argv[1]
baseUrl = 'http://%s:9200/%s/%s/' % (sys.argv[2], sys.argv[3], sys.argv[4])

DEFAULT_DATE = '"1990-11-11T00:00:00.000Z"'


def conv_date(afair: str) -> str:
    """Convert date format in JSON file created from MongoDB
    convert
        "timeStart":{"$date":"2015-09-01T00:00:00.000Z"}
    to: "timeStart":"2015-09-01T00:00:00.000Z"
    """
    trans_normal = re.sub(
            r'{"\$date":("2\d\d\d-\d\d-\d\dT\d\d:\d\d:\d\d.\d\d\dZ")}',
            r'\1',
            afair)
    # 不符合标准格式的日期全部强制转换为默认日期
    return re.sub(r'{"\$date":(".*?")}', DEFAULT_DATE, trans_normal)

with open(inp) as f:
    RECUR = 'recurrence'
    TIMES = 'timeStart'
    cnt = 0
    for line in f:
        fair = json.loads(conv_date(line.strip()))
        if RECUR not in fair:
            continue
        recs = fair[RECUR]
        fair[RECUR] = sorted(recs,
                             key=lambda rec: rec[TIMES] if TIMES in rec
                             else DEFAULT_DATE,
                             reverse=True)
        fairID = fair['_id']
        cnt = cnt + 1
        print('uploading No. %d: %s ...' % (cnt, fairID))
        targetUrl = baseUrl + fairID
        del fair['_id']
        res = requests.post(targetUrl, data=json.dumps(fair)).json()
        if 'status' in res:
            print('upload error for %s: %s' % (fairID, res['error']),
                  file=sys.stderr)
