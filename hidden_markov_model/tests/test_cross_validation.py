import glob
import unittest

import re
from hidden_markov_model.pos_tagger import POSTagger


class TestCrossValidation(unittest.TestCase):
  FOLDS = 10

  def setUp(self):
    self.files = glob.glob('data/brown/c???')

  def test(self):
    for i in range(TestCrossValidation.FOLDS):
      print("test cross validation for fold %d" % i)
      splits = int(len(self.files) / TestCrossValidation.FOLDS)
      validation_indexes = range(i * splits, (i + 1) * splits)

      training_indexes = list(set(range(len(self.files))).difference(validation_indexes))
      validation_files = [fn for idx, fn in enumerate(self.files)
                          if idx in validation_indexes]
      training_files = [fn for idx, fn in enumerate(self.files)
                        if idx in training_indexes]

      pos_tagger = POSTagger.from_filepaths(training_files, True)

      misses = 0
      successes = 0

      for vf in validation_files:
        with open(vf, 'r') as f:
          for l in f:
            if re.match(r'\A\s+\Z', l):
              continue
            words = []
            parts_of_speech = ['START']
            for ppp in re.split(r'\s+', l.strip()):
              z = ppp.split('/')
              words.append(z[0])
              parts_of_speech.append(z[1])

            tag_seq = pos_tagger.viterbi(' '.join(words))
            for tag1, tag2 in zip(tag_seq, parts_of_speech):
              if tag1 == tag2:
                successes += 1
              else:
                misses += 1
        print(misses / float(misses + successes))
      print('Error rate was %f' % (misses / float(misses + successes)))
