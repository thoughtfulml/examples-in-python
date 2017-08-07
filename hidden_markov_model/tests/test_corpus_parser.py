import unittest

from corpus_parser import CorpusParser


class TestCorpusParser(unittest.TestCase):
  def setUp(self):
    self.stream = '\tSeveral/ap defendants/nns ./.\n'
    self.blank = '\t    \n'

  def test_parse(self):
    """will parse a brown corpus line using the standard / notation"""
    cp = CorpusParser()

    null = CorpusParser.TagWord('START', 'START')
    several = CorpusParser.TagWord('Several', 'ap')
    defendants = CorpusParser.TagWord('defendants', 'nns')
    period = CorpusParser.TagWord('.', '.')

    expectations = [
      [null, several],
      [several, defendants],
      [defendants, period]
    ]

    results = list(cp.parse(self.stream))
    self.assertListEqual(expectations, results)

  def test_blank(self):
    """does not allow blank lines from happening"""
    cp = CorpusParser()

    results = list(cp.parse(self.blank))
    self.assertEqual(0, len(results))
