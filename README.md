# Sync with RESTful API of ES

Sync all documents in MongoDB into Elasticsearch database.
The fair's recurrences will be sorted in descending order by the 'timeStart' field.

# Usage

First, export MongoDB documents to a json file:

```bash
mongoexport -h 192.168.100.3 -d production -c Fair -u dba -p dba -o fairs.json
```

Then upload data to Elasticsearch, exclude all the docs whose 'recurrence.timeStart'
property contains 2013, 2014 or 2015.

```bash
python3 uploadES.py fairs.json --server 123,34.45.6 --index production --type shops --exclude 2008,2009,2010,2011,2012,2013,2014,2015
```

Run `python3 uploadES.py -h` for help.

# Notes

## Partial Export

You can export some of the MongoDB documents with
`mongoexport -h 192.168.100.3 -d production -c Fair -u dba -p dba -o fairs.json --limit 100`.

## When uploading fails

If some documents can't be uploaded to ES server for the mapping mismatch,
try the following steps:

1. Get the current mapping, check it and modify it when necessary;

1. Buld a new index, set its mappings with the file you created in above step;

1. Upload your data with this script.

## Debug

To verify the converted date format, replace all codes below `for line in f:`
in file uploadES.py with `print(conv_date(line.strip()))`.
Save the converting result in file "rightDate.json":
`python3 uploadES.py fairs.json production Fair > rightDate.json`.
Importing it into a temporary database:
`mongoimport -d test -c strDate --type json --file rightDate.json`
The date is converted successfully if no errors occurs.
