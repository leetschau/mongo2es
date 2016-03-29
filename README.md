# Introduction

# upload with elasticdump

Step 1: export MongoDB data to json file:

```bash
mongoexport -h 192.168.100.3 -d production -c Fair -u dba -p dba -o fairs.json --jsonArray
```

Or select some data to export:
```bash
mongoexport -h 192.168.100.3 -d production -c Fair -u dba -p dba -q '{_id: "9Jox43DBwBznf9t3X"}' -o afair.json --jsonArray
```

Step 2: convert them to ES format:

```bash
node main.js <input-file> <output-file> <index-name> <type-name>
```

Step 3: upload to ES with elasticdump:

```bash
npm install -g elasticdump
elasticdump --bulk=true --input=./esfs.json --output=http://192.168.100.24:9200/
```

# Sync to ES one by one

Step 1: export MongoDB data to json file:

```bash
mongoexport -h 192.168.100.3 -d production -c Fair -u dba -p dba -o fairs.json
```

Or only export some with `--limit` option:

```bash
mongoexport -h 192.168.100.3 -d production -c Fair -u dba -p dba -o fairs.json --limit 100
```

Step 2: create ES index with mapping:

```bash
curl -XPOST http://192.168.100.24:9200/test -d '@esFairMapping.json'
```

Step 3: upload data:

Modify parameter names in uploadES.py and run:

```bash
python uploadES.py
```

TODO: use [ES bulk API](https://www.elastic.co/guide/en/elasticsearch/reference/current/docs-bulk.html)
to promote efficiency.
