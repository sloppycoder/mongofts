import unittest

from gen_rand_trans import *
from essential_generators import DocumentGenerator
import random


class MyTest(unittest.TestCase):
    gen = DocumentGenerator()

    def test_default_args(self):
        params = ['-n', '5']
        opts = parse_args(params)
        self.assertEqual(DEFAULT_AVG, opts.avg)
        self.assertFalse(opts.drop)

    def test_custom_args(self):
        params = ['-n', '5', '--avg', '99', '--drop']
        opts = parse_args(params)
        self.assertEqual(5, opts.n)
        self.assertEqual(99, opts.avg)
        self.assertTrue(opts.drop)

    def test_gen_account_ids(self):
        ids = gen_account_ids(self.gen, 1000)
        uniq_ids = list(set(ids))
        self.assertEqual(1000, len(uniq_ids))

    def test_new_tran(self):
        tran = new_tran(self.gen, '1000')
        self.assertIsNotNone(tran)
        self.assertIsNotNone(tran['memo'])

    def test_gen_batch_1(self):
        n = gen_random_trans(1, 3, batch_size=2)
        batch1 = next(n)
        self.assertEqual(2, len(batch1), "batch1 does not have the right size")
        batch2 = next(n)
        self.assertEqual(1, len(batch2), "batch2 does not have the right size")

    def test_gen_batch_2(self):
        n = gen_random_trans(2, 2, batch_size=2)
        batch1 = next(n)
        self.assertEqual(2, len(batch1), "batch1 does not have the right size")
        batch2 = next(n)
        self.assertEqual(2, len(batch2), "batch2 does not have the right size")
        with self.assertRaises(StopIteration):
            next(n)

    @unittest.skip('need a database with test data to run this test')
    def test_search(self):
        collection = mongo_collection()
        ids = get_all_ids(collection, limit=100)
        hit = 0
        for i in range(0, 10):
            length = random.randrange(1, 2)
            account_no = ids[random.randrange(0, len(ids))]
            search_term = self.gen.word()[:length]
            matches = [t for t in
                       collection.find({'account_no': account_no,
                                        '$text': {'$search': search_term}})]
            if len(matches) > 0:
                hit += 1
        print(f'hits = {hit}')


if __name__ == '__main__':
    unittest.main()
