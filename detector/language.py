# coding=UTF-8

from tokenizer import Tokenizer

class Language:
  def __init__(self, language_io, name):
    self.name = name
    self.vectors, self.characters = Tokenizer.tokenize(language_io)
