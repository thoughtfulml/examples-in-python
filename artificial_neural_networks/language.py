from tokenizer import Tokenizer


class Language(object):
  def __init__(self, io, name):
    self._name = name
    self._vectors, self._characters = Tokenizer.tokenize(io)

  @property
  def name(self): return self._name

  @property
  def vectors(self): return self._vectors

  @property
  def characters(self): return self._characters
