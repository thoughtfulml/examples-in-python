# coding=UTF-8
from collections import defaultdict

class Tokenizer:
  PUNCTUATION = ["~", "@", "#", "$", "%", "^", "&", "*", "(", ")", "_", "+", "'", "[", "]", "<", ">", "/", "\\", u"“", u"”", u"‘", u"’", u"»", u"«", u"›", u"‹", u"–", u"„", u"—"]
  SPACES = [" ", u"\u00A0", "\n"]
  STOP_CHARACTERS = ['.', '?', '!']

  @staticmethod
  def tokenize(io):
    vectors = []

    dist = defaultdict(lambda: 0, {})

    characters = set()

    for line in io.readlines():
      for char in line:
        if char in Tokenizer.STOP_CHARACTERS:
          if dist:
            vectors.append(Tokenizer.normalize(dist))
          dist = defaultdict(lambda: 0, {})
        elif char in Tokenizer.SPACES or char in Tokenizer.PUNCTUATION:
          "Nothing to do here"
        else:
          character = char.lower()
          characters.add(character)
          dist[character] += 1
    if dist:
      vectors.append(Tokenizer.normalize(dist))
    return [vectors, characters]

  @staticmethod
  def normalize(dictionary):
    total = float(sum(dictionary.values()))

    return dict([k, v / total] for k,v in dictionary.iteritems())
