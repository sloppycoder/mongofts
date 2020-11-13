from datetime import datetime

import pymongo
from common import gen_random_trans, parse_args, DEFAULT_MONGODB_URL


# globals
mongo_client = None


def search_trans(collection, account_no, keyword):
    return [
        t
        for t in collection.find(
            {"account_no": account_no, "$text": {"$search": keyword}}
        )
    ]


def create_rand_trans(mongodb_url, num_of_accounts, avg_per_account, force_drop=False):
    collection = mongo_collection(mongodb_url)
    if force_drop:
        collection.drop()
    for batch in gen_random_trans(num_of_accounts, avg_per_account):
        collection.insert_many(batch)
        print(f"{str(datetime.now())[:23]} - written {len(batch)} documents")


def get_all_ids(collection, limit=0):
    """
    retrieve a list of account no from collection
    """
    ids = []
    for tran in collection.find({}, {"account_no": 1}).limit(limit):
        ids.append(tran["account_no"])
    print(f"using {len(ids)} account numbers")
    return ids


def mongo_collection(mongodb_url=DEFAULT_MONGODB_URL):
    global mongo_client
    mongo_client = pymongo.MongoClient(mongodb_url)
    import atexit

    atexit.register(mongo_client.close)
    return mongo_client.dev.transactions


if __name__ == "__main__":
    import sys

    args = parse_args(sys.argv[1:])
    create_rand_trans(args.db, args.n, args.avg, args.drop)
