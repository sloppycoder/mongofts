import pytest
from gen_rand_trans import *


@pytest.mark.benchmark(
    min_time=0.1,
    max_time=0.5,
    min_rounds=10,
)
def test_search(benchmark):
    collection = mongo_collection()
    ids = get_all_ids(collection, limit=100000)
    for tran in collection.find({}, {'account_no': 1}):
        ids.append(tran['account_no'])
    print(f'using {len(ids)} account numbers')
    gen = DocumentGenerator()
    result = benchmark(search, collection, ids, gen, loop=100)
    print(result)
    assert result > 0


def search(collection, ids, gen, loop=10):
    hit = 0
    total = len(ids)
    for i in range(0, loop):
        length = random.randrange(2, 6)
        account_no = ids[random.randrange(0, total)]
        keyword = gen.word()[:length]
        matches = search_trans(collection, account_no, keyword)
        hit += len(matches)
    return hit


if __name__ == '__main__':
    import sys
    pytest.main(sys.argv)