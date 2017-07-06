from io import StringIO
import unittest

from numpy import array

from scipy.sparse import csr_matrix

from support_vector_machines.corpus import Corpus
from support_vector_machines.corpus_set import CorpusSet


class TestCorpusSet(unittest.TestCase):
    def setUp(self):
        self.positive = StringIO('I love this country')
        self.negative = StringIO('I hate this man')

        self.positive_corp = Corpus(self.positive, 'positive')
        self.negative_corp = Corpus(self.negative, 'negative')

        self.corpus_set = CorpusSet([self.positive_corp, self.negative_corp])

    def test_compose(self):
        """composes two corpuses together"""
        self.assertEqual({'love', 'country', 'hate', 'man'},
                         self.corpus_set.words)

    def test_spars(self):
        """returns a set of sparse vectors to train on"""
        expected_ys = [1, -1]
        expected_xes = csr_matrix(array(
            [[1, 1, 0, 0],
             [0, 0, 1, 1]]
        ))

        self.corpus_set.calculate_sparse_vectors()
        ys = self.corpus_set.yes
        xes = self.corpus_set.xes

        self.assertListEqual(expected_ys, ys)
        self.assertListEqual(list(expected_xes.data),
                             list(xes.data))
        self.assertListEqual(list(expected_xes.indices),
                             list(xes.indices))
        self.assertListEqual(list(expected_xes.indptr),
                             list(xes.indptr))
