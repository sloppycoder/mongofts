## test MongoDB text index

```
# install mongo commnity edition

mongo < user.js

# enable security, restart mongod

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# generate 10000 accounts, which about 1000 transactions per account on average
# for mongodb
python mongo_rand_trans.py -n 10000 --avg 1000

# for elastic
# the current version does not use bulk api and is much slower compared to the mongo version
python es_rand_trans.py -n 10000 --avg 1000

mongo -u dev -p dev dev < index.js

py.test benchmark.py

# should show some benchmark numbers
```

## storage usage

for MongoDB, the storage usage

```
> db.transactions.count()
10000000
> db.runCommand( {dbStats: 1, scale:1024*1024} )
{
	"db" : "dev",
	"collections" : 3,
	"views" : 0,
	"objects" : 10000003,
	"avgObjSize" : 173.8285896514231,
	"dataSize" : 1657.759111404419,
	"storageSize" : 975.8046875,
	"indexes" : 4,
	"indexSize" : 3025.92578125,
	"totalSize" : 4001.73046875,
	"scaleFactor" : 1048576,
	"fsUsedSize" : 126940.859375,
	"fsTotalSize" : 361337.46875,
	"ok" : 1
}
```

for Elastic Search
```
$ curl http://127.0.0.1:9200/transactions/_stats | jq '.indices.transactions.total | .docs, .store'

100  8923  100  8923    0     0  4356k      0 --:--:-- --:--:-- --:--:-- 4356k
{
  "count": 10000739,
  "deleted": 0
}
{
  "size_in_bytes": 3023095170,
  "reserved_in_bytes": 0
}

$ curl http://127.0.0.1:9200/_cat/allocation\?v
shards disk.indices disk.used disk.avail disk.total disk.percent host      ip        node
     7        2.8gb   128.2gb    224.6gb    352.8gb           36 127.0.0.1 127.0.0.1 gf63
     1                                                                               UNASSIGNED

```
