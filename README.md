## test MongoDB text index 

```
# install mongo commnity edition

mongo < user.js

# enable security, restart mongod

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# generate 10000 accounts, which about 1000 transactions per account on average
python gen_rand_trans.py -n 10000 --avg 1000

mongo -u dev -p dev dev < index.js

py.test benchmark.py

# should show some benchmark numbers
```
