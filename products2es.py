import requests
import argparse
import json
import re
import sys

parser = argparse.ArgumentParser(
    description='Sync product collection in MongoDB to Elasticsearch server')
parser.add_argument('inputfile',
                    help='the json file contains data to synced from MongoDB')
parser.add_argument('-s', '--server',
                    help='the IP address of Elasticsearch server')
parser.add_argument('-i', '--index', help='the index name of ES')
parser.add_argument('-t', '--typename', help='the type name of the index')
args = parser.parse_args()

baseUrl = 'http://%s:9200/%s/%s/' % (args.server, args.index, args.typename)

DEFAULT_DATE = '"1990-11-11T00:00:00.000Z"'
RECUR = 'recurrence'
TIMES = 'timeStart'


def conv_date(afair: str) -> str:
    """Convert date format in JSON file created from MongoDB
    convert
        "timeStart":{"$date":"2015-09-01T00:00:00.000Z"}
    to: "timeStart":"2015-09-01T00:00:00.000Z"
    """
    # 转换标准格式的日期
    trans_normal = re.sub(
            r'{"\$date":("2\d\d\d-\d\d-\d\dT\d\d:\d\d:\d\d.\d\d\dZ")}',
            r'\1',
            afair)
    # 不符合标准格式的日期全部强制转换为默认日期
    return re.sub(r'{"\$date":(".*?")}', DEFAULT_DATE, trans_normal)

if __name__ == "__main__":
    with open(args.inputfile) as f:
        cnt = 0
        for line in f:
            product = json.loads(conv_date(line.strip()))
            productId = product['_id']
            cnt = cnt + 1
            print('uploading No. %d: %s ...' % (cnt, productId))
            targetUrl = baseUrl + productId
            del product['_id']

            res = requests.post(targetUrl, data=json.dumps(product)).json()
            if 'status' in res:
                print('upload error for %s: %s' % (fairId, res['error']),
                      file=sys.stderr)
