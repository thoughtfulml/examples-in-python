from StringIO import StringIO
import unittest

from corpus import Corpus


class TestCorpusSet(unittest.TestCase):
    def setUp(self):
        self.negative = StringIO('I hated that so much')
        self.negative_corpus = Corpus(self.negative, 'negative')
        self.positive = StringIO('loved movie!! loved')
        self.positive_corpus = Corpus(self.positive, 'positive')

    def test_trivial(self):
        """consumes multiple files and turns it into sparse vectors"""
        self.assertEqual('negative', self.negative_corpus.sentiment)

    def test_tokenize1(self):
        """downcases all the word tokens"""
        self.assertListEqual(['quick', 'brown', 'fox'], Corpus.tokenize('Quick Brown Fox'))

    def test_tokenize2(self):
        """ignores all stop symbols"""
        self.assertListEqual(['hello'], Corpus.tokenize('"\'hello!?!?!.\'"  '))

    def test_tokenize3(self):
        """ignores the unicode space"""
        self.assertListEqual(['hello', 'bob'], Corpus.tokenize(u'hello\u00A0bob'))

    def test_positive(self):
        """consumes a positive training set"""
        self.assertEqual('positive', self.positive_corpus.sentiment)

    def test_words(self):
        """consumes a positive training set and unique set of words"""
        self.assertEqual({'loved', 'movie'}, self.positive_corpus.get_words())

    def test_sentiment_code_1(self):
        """defines a sentiment_code of 1 for positive"""
        self.assertEqual(1, Corpus(StringIO(''), 'positive').sentiment_code)

    def test_sentiment_code_minus1(self):
        """defines a sentiment_code of 1 for positive"""
        self.assertEqual(-1, Corpus(StringIO(''), 'negative').sentiment_code)
