from StringIO import StringIO
import unittest

from pos_tagger import POSTagger


class TestViterbi(unittest.TestCase):
    def setUp(self):
        self.training = 'I/PRO want/V to/TO race/V ./. I/PRO like/V cats/N ./.'
        self.sentence = 'I want to race.'
        self.pos_tagger = POSTagger([StringIO(self.training)])
        self.pos_tagger.train()

    def test(self):
        """will calculate the best viterbi sequence for I want to race"""
        expectation = ['START', 'PRO', 'V', 'TO', 'V', '.']
        result = self.pos_tagger.viterbi(self.sentence)
        self.assertListEqual(expectation, result)


class TestProbabilityCalculation(unittest.TestCase):
    def setUp(self):
        self.stream = 'A/B C/D C/D A/D A/B ./.'
        self.pos_tagger = POSTagger([StringIO(self.stream)])
        self.pos_tagger.train()

    def test1(self):
        """calculates tag transition probabilities"""
        self.assertAlmostEqual(0, self.pos_tagger.tag_probability('Z', 'Z'))
        self.assertAlmostEqual(2.0 / 3, self.pos_tagger.tag_probability('D', 'D'))
        self.assertAlmostEqual(1, self.pos_tagger.tag_probability('START', 'B'))
        self.assertAlmostEqual(0.5, self.pos_tagger.tag_probability('B', 'D'))
        self.assertAlmostEqual(0, self.pos_tagger.tag_probability('.', 'D'))

    def test2(self):
        """calculates probability of sequence of words and tags"""
        words = ['START', 'A', 'C', 'A', 'A', '.']
        tags = ['START', 'B', 'D', 'D', 'B', '.']
        tag_probabilities = self.pos_tagger.tag_probability('B', 'D') * \
                            self.pos_tagger.tag_probability('D', 'D') * \
                            self.pos_tagger.tag_probability('D', 'B') * \
                            self.pos_tagger.tag_probability('B', '.')
        word_probabilities = self.pos_tagger.word_tag_probability('A', 'B') * \
                             self.pos_tagger.word_tag_probability('C', 'D') * \
                             self.pos_tagger.word_tag_probability('A', 'D') * \
                             self.pos_tagger.word_tag_probability('A', 'B')
        expected = word_probabilities * tag_probabilities
        result = self.pos_tagger.probability_of_word_tag(words, tags)
        self.assertAlmostEqual(expected, result)

    def test3(self):
        """calculates the probability of a word given a tag"""
        self.assertAlmostEqual(0, self.pos_tagger.word_tag_probability('Z', 'Z'))
        self.assertAlmostEqual(1, self.pos_tagger.word_tag_probability('A', 'B'))
        self.assertAlmostEqual(1.0 / 3, self.pos_tagger.word_tag_probability('A', 'D'))
        self.assertAlmostEqual(1, self.pos_tagger.word_tag_probability('.', '.'))
