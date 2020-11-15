from datetime import datetime
import uuid

from elasticsearch import Elasticsearch
from common import gen_random_trans, parse_args

INDEX_NAME = "transactions"

# globals
es = Elasticsearch()


def search_trans(collection, account_no, keyword):
    return []


def create_rand_trans(es_url, num_of_accounts, avg_per_account, force_drop=False):
    global es
    if force_drop:
        es.indices.delete(index=INDEX_NAME, ignore=[400, 404])
    for batch in gen_random_trans(num_of_accounts, avg_per_account):
        for item in batch:
            es.index(index=INDEX_NAME, id=uuid.uuid4(), body=item)
        print(f"{str(datetime.now())[:23]} - written {len(batch)} documents")
        es.indices.refresh(index=INDEX_NAME)


def get_all_ids(collection, limit=0):
    """
    retrieve a list of account no from collection
    """
    ids = []
    return ids


if __name__ == "__main__":
    import sys

    args = parse_args(sys.argv[1:])
    create_rand_trans(args.db, args.n, args.avg, args.drop)
