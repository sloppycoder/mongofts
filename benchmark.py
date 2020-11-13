import random

import pytest

from gen_rand_trans import gen, get_all_ids, mongo_collection, search_trans


@pytest.mark.benchmark(
    min_time=0.1,
    max_time=0.5,
    min_rounds=10,
)
def test_search(benchmark):
    collection = mongo_collection()
    ids = get_all_ids(collection, limit=100000)
    loop = 100
    hits = benchmark(search, collection, ids, loop=loop)
    print(f"loop={loop} search hits = {hits}")
    assert hits > 0


def search(collection, ids, loop=10):
    """
    perform a search on collection with account no and keyword
    account no is randomly picked ids
    search keyword is the first N (2 <= N <= 6) chars from a random word
    """
    hit = 0
    total = len(ids)
    for i in range(0, loop):
        length = random.randrange(2, 6)
        account_no = ids[random.randrange(0, total)]
        keyword = gen.word()[:length]
        matches = search_trans(collection, account_no, keyword)
        hit += len(matches)
    return hit


if __name__ == "__main__":
    import sys

    pytest.main(sys.argv)
