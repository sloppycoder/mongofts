import pymongo
import argparse
import random
import sys
from datetime import datetime, timedelta
from essential_generators import DocumentGenerator

MONGODB_URL = 'mongodb://dev:dev@localhost:27017/dev?authSource=dev'
BATCH_SIZE = 1000
LAST_TS = datetime.utcnow()
TS_RANGE = 3600 * 30 * 3 + 1  # seconds in 3 months
DEFAULT_AVG = 50
mongo_client = None


def gen_account_ids(gen, num_of_accounts):
    ids = []
    for i in range(0, num_of_accounts):
        ids.append(gen.phone().replace('-', '') + str(random.randrange(10000, 19999)))
    return ids


def new_tran(gen, account_no):
    secs = random.randrange(0, TS_RANGE)
    return {
        'account_no': account_no,
        'timestamp': LAST_TS - timedelta(seconds=secs),
        'amount': random.randrange(1000, 1000000),
        'currency': 'THB',
        'memo': gen.sentence()
    }


def gen_random_trans(num_of_accounts, avg_per_account, batch_size=BATCH_SIZE):
    gen = DocumentGenerator()
    total = num_of_accounts * avg_per_account
    ids = gen_account_ids(gen, num_of_accounts)
    bulk = []
    for i in range(0, total):
        n = random.randrange(0, num_of_accounts)
        bulk.append(new_tran(gen, ids[n]))
        if len(bulk) == batch_size or i >= total - 1:
            yield bulk
            bulk.clear()


def search_trans(collection, account_no, keyword):
    return [t for t in collection.find({'account_no': account_no,
                                        '$text': {'$search': keyword}})]


def create_rand_trans(mongodb_url, num_of_accounts, avg_per_account, force_drop=False):
    collection = mongo_collection(mongodb_url)
    if force_drop:
        collection.drop()
    for batch in gen_random_trans(num_of_accounts, avg_per_account):
        collection.insert_many(batch)
        print(f'{str(datetime.now())[:23]} - written {len(batch)} documents')


def get_all_ids(collection, limit=0):
    ids = []
    for tran in collection.find({}, {'account_no': 1}).limit(limit):
        ids.append(tran['account_no'])
    print(f'using {len(ids)} account numbers')
    return ids


def mongo_collection(mongodb_url=MONGODB_URL):
    global mongo_client
    mongo_client = pymongo.MongoClient(mongodb_url)
    import atexit
    atexit.register(mongo_client.close)
    return mongo_client.dev.transactions


def parse_args(args):
    parser = argparse.ArgumentParser(description='Generate random transactions and store them in mongo')
    parser.add_argument('--db', default=MONGODB_URL, metavar='MONGODB_URL')
    parser.add_argument('-n', type=int, metavar='NUM_OF_ACCOUNTS',
                        help='number of accounts to generate')
    parser.add_argument('--avg', type=int, default=DEFAULT_AVG, metavar='TRANSACTION_PER_ACCOUNT',
                        help='average number of accounts to generate')
    parser.add_argument('--drop', default=False, action='store_true',
                        help='drop existing collection')
    return parser.parse_args(args)


if __name__ == '__main__':
    random.seed(LAST_TS.microsecond)
    args = parse_args(sys.argv[1:])
    create_rand_trans(args.db, args.n, args.avg, args.drop)
