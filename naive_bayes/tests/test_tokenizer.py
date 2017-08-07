import unittest

from tokenizer import Tokenizer


class TestTokenizer(unittest.TestCase):
  def setUp(self):
    self.string = "this is a test of the emergency broadcasting system"

  def test_downcasing(self):
    expectation = ["this", "is", "all", "caps"]

    actual = Tokenizer.tokenize("THIS IS ALL CAPS")
    self.assertEqual(actual, expectation)

  def test_ngrams(self):
    expectation = [
      [u'\u0000', "quick"],
      ["quick", "brown"],
      ["brown", "fox"],
    ]

    actual = Tokenizer.ngram("quick brown fox", 2)
    self.assertEqual(actual, expectation)
