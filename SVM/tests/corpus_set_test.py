from StringIO import StringIO
import unittest

from corpus import Corpus
from corpus_set import CorpusSet


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
        expected_xes = [[0, 1], [2, 3]]
        expected_xes = [{a: 1 for a in b} for b in expected_xes]

        ys, xes = self.corpus_set.to_sparse_vectors()

        self.assertListEqual(expected_ys, ys)


'''
require_relative './spec_helper'

describe CorpusSet do
  let(:positive) { StringIO.new('I love this country') }
  let(:negative) { StringIO.new('I hate this man') }

  let(:positive_corp) { Corpus.new(positive, :positive) }
  let(:negative_corp) { Corpus.new(negative, :negative) }

  let(:corpus_set) { CorpusSet.new([positive_corp, negative_corp]) }

  it 'composes two corpuses together' do
    corpus_set.words.must_equal %w[love country hate man]
  end

  it 'returns a set of sparse vectors to train on' do
    expected_ys = [1, -1]
    expected_xes = [[0,1], [2,3]]
    expected_xes.map! do |x|
      Libsvm::Node.features(Hash[x.map {|i| [i, 1]}])
    end

    ys, xes = corpus_set.to_sparse_vectors

    ys.must_equal expected_ys

    xes.flatten.zip(expected_xes.flatten).each do |x, xp|
      x.value.must_equal xp.value
      x.index.must_equal xp.index
    end
  end
end
'''
