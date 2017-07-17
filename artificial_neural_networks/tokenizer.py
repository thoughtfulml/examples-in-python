# coding=utf-8
from fractions import Fraction

import collections


class Tokenizer(object):
  punctuation = list(u'~@#$%^&*()_+\'[]“”‘’—<>»«›‹–„/')
  spaces = list(u' \u00A0\n')
  stop_characters = list('.?!')

  @classmethod
  def tokenize(cls, io):
    vectors = []
    dist = collections.defaultdict(int)
    characters = set()

    for char in io.read():
      if char in cls.stop_characters:
        if len(dist) > 0:
          vectors.append(cls.normalize(dist))
          dist = collections.defaultdict(int)
      elif char not in cls.spaces and char not in cls.punctuation:
        character = char.lower()
        characters.add(character)
        dist[character] += 1
    if len(dist) > 0:
      vectors.append(cls.normalize(dist))

    return vectors, characters

  @classmethod
  def normalize(cls, dist):
    sum_values = sum(dist.values())
    return {k: Fraction(v, sum_values) for k, v in dist.items()}
