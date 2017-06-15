import unittest

import io
from naive_bayes.email_object import EmailObject
from naive_bayes.spam_trainer import SpamTrainer


class TestSpamTrainer(unittest.TestCase):
  def setUp(self):
    self.training = [['spam', './tests/fixtures/plain.eml'], ['ham', './tests/fixtures/small.eml'],
                     ['scram', './tests/fixtures/plain.eml']]
    self.trainer = SpamTrainer(self.training)
    with io.open('./tests/fixtures/plain.eml', 'rb') as eml_file:
      self.email = EmailObject(eml_file)

  def test_multiple_categories(self):
    categories = self.trainer.categories
    expected = set([k for k, v in self.training])
    self.assertEqual(categories, expected)

  def test_counts_all_at_zero(self):
    for cat in ['_all', 'spam', 'ham', 'scram']:
      self.assertEqual(self.trainer.total_for(cat), 0)

  def test_preference_category(self):
    trainer = self.trainer
    expected = sorted(trainer.categories, key=lambda cat: trainer.total_for(cat))

    self.assertEqual(trainer.preference(), expected)

  def test_probability_being_1_over_n(self):
    trainer = self.trainer
    scores = list(trainer.score(self.email).values())

    self.assertAlmostEqual(scores[0], scores[-1])

    for i in range(len(scores) - 1):
      self.assertAlmostEqual(scores[i], scores[i + 1])

  def test_adds_up_to_one(self):
    trainer = self.trainer
    scores = list(trainer.normalized_score(self.email).values())
    self.assertAlmostEqual(sum(scores), 1)
    self.assertAlmostEqual(scores[0], 1 / 2.0)

  def test_give_preference_to_whatever_has_the_most(self):
    trainer = self.trainer
    score = trainer.score(self.email)

    preference = trainer.preference()[-1]
    preference_score = score[preference]

    expected = SpamTrainer.Classification(preference, preference_score)
    self.assertEqual(trainer.classify(self.email), expected)
