import random
from datetime import datetime, timedelta

from essential_generators import DocumentGenerator

BATCH_SIZE = 1000
LAST_TS = datetime.utcnow()
TS_RANGE = 3600 * 30 * 3 + 1  # seconds in 3 months
DEFAULT_AVG = 50
DEFAULT_MONGODB_URL = "mongodb://dev:dev@localhost:27017/dev?authSource=dev"
DEFAULT_ES_URL = "http://127.0.0.1:9300"


gen = DocumentGenerator()


def gen_account_ids(num_of_accounts):
    """
    generate a list of unique account numbers
    """
    ids = []
    for i in range(0, num_of_accounts):
        ids.append(gen.phone().replace("-", "") + str(random.randrange(10000, 19999)))
    return ids


def new_tran(account_no):
    """
    generate a new transaction with randomly generated data
    """
    secs = random.randrange(0, TS_RANGE)
    return {
        "account_no": account_no,
        "timestamp": LAST_TS - timedelta(seconds=secs),
        "amount": random.randrange(1000, 1000000),
        "currency": "THB",
        "memo": gen.sentence(),
    }


def gen_random_trans(num_of_accounts, avg_per_account, batch_size=BATCH_SIZE):
    """
    generate random transactions
    and return them in list up to batch_size entries
    using generator

    The total number of transactions will be num_of_accounts * avg_per_account
    """
    total = num_of_accounts * avg_per_account
    ids = gen_account_ids(num_of_accounts)
    bulk = []
    for i in range(0, total):
        n = random.randrange(0, num_of_accounts)
        bulk.append(new_tran(ids[n]))
        if len(bulk) == batch_size or i >= total - 1:
            yield bulk
            bulk.clear()


def parse_args(args):
    from argparse import ArgumentParser

    parser = ArgumentParser(
        description="Generate random transactions and store them in mongo or elastic"
    )
    parser.add_argument("--type", default="mongo", metavar="DB_TYPE")
    parser.add_argument("--db", default=DEFAULT_MONGODB_URL, metavar="MONGODB_URL")

    parser.add_argument(
        "-n", type=int, metavar="NUM_OF_ACCOUNTS", help="number of accounts to generate"
    )
    parser.add_argument(
        "--avg",
        type=int,
        default=DEFAULT_AVG,
        metavar="TRANSACTION_PER_ACCOUNT",
        help="average number of accounts to generate",
    )
    parser.add_argument(
        "--drop", default=False, action="store_true", help="drop existing collection"
    )
    return parser.parse_args(args)
