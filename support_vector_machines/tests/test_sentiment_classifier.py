from fractions import Fraction
import unittest

import io
import os
from sentiment_classifier import SentimentClassifier


class TestSentimentClassifier(unittest.TestCase):
  def setUp(self):
    pass

  def test_validate(self):
    """cross validates with an error of 35% or less"""
    neg = self.split_file('data/rt-polaritydata/rt-polarity.neg')
    pos = self.split_file('data/rt-polaritydata/rt-polarity.pos')

    classifier = SentimentClassifier.build([
      neg['training'],
      pos['training']
    ])

    c = 2 ** 7
    classifier.c = c
    classifier.reset_model()

    n_er = self.validate(classifier, neg['validation'], 'negative')
    p_er = self.validate(classifier, pos['validation'], 'positive')
    total = Fraction(n_er.numerator + p_er.numerator,
                     n_er.denominator + p_er.denominator)
    print(total)
    self.assertLess(total, 0.35)

  def test_validate_itself(self):
    """yields a zero error when it uses itself"""
    classifier = SentimentClassifier.build([
      'data/rt-polaritydata/rt-polarity.neg',
      'data/rt-polaritydata/rt-polarity.pos'
    ])

    c = 2 ** 7
    classifier.c = c
    classifier.reset_model()

    n_er = self.validate(classifier,
                         'data/rt-polaritydata/rt-polarity.neg',
                         'negative')
    p_er = self.validate(classifier,
                         'data/rt-polaritydata/rt-polarity.pos',
                         'positive')
    total = Fraction(n_er.numerator + p_er.numerator,
                     n_er.denominator + p_er.denominator)
    print(total)
    self.assertEqual(total, 0)

  def validate(self, classifier, file, sentiment):
    total = 0
    misses = 0

    with(open(file, errors='ignore')) as f:
      for line in f:
        if classifier.classify(line) != sentiment:
          misses += 1
        total += 1
    return Fraction(misses, total)

  def split_file(self, filepath):
    ext = os.path.splitext(filepath)[1]
    counter = 0
    training_filename = 'tests/fixtures/training%s' % ext
    validation_filename = 'tests/fixtures/validation%s' % ext
    with(io.open(filepath, errors='ignore')) as input_file:
      with(io.open(validation_filename, 'w')) as val_file:
        with(io.open(training_filename, 'w')) as train_file:
          for line in input_file:
            if counter % 2 == 0:
              val_file.write(line)
            else:
              train_file.write(line)
            counter += 1
    return {'training': training_filename,
            'validation': validation_filename}
