import numpy as np
import theanets

from tokenizer import Tokenizer


class Network(object):
  def __init__(self, languages, error=0.005):
    self._trainer = None
    self._net = None
    self.languages = languages
    self.error = error
    self.inputs = set()
    for language in languages:
      self.inputs.update(language.characters)
    self.inputs = sorted(self.inputs)

  def train(self):
    self._build_trainer()
    self._build_ann()
    self._net.train(self._trainer, learning_rate=0.01)

  def predict(self, sentence):
    if self._net is None or self._trainer is None:
      raise Exception('Must train first')
    vectors, characters = Tokenizer.tokenize(sentence)
    if len(vectors) == 0:
      return None
    input = np.array(self._code(vectors[0]),
                     ndmin=2,
                     dtype=np.float32)
    result = self._net.predict(input)
    return self.languages[result[0]]

  def _build_trainer(self):
    inputs = []
    desired_outputs = []
    for language_index, language in enumerate(self.languages):
      for vector in language.vectors:
        inputs.append(self._code(vector))
        desired_outputs.append(language_index)
    inputs = np.array(inputs, dtype=np.float32)
    desired_outputs = np.array(desired_outputs, dtype=np.int32)
    self._trainer = (inputs, desired_outputs)

  def _code(self, vector):
    result = np.zeros(len(self.inputs))
    for char, freq in vector.items():
      if char in self.inputs:
        result[self.inputs.index(char)] = float(freq)
    return result

  def _build_ann(self):
    hidden_neurons = 2 * (len(self.inputs) + len(self.languages)) / 3

    self._net = theanets.Classifier([len(self.inputs),
                                     {'size': int(hidden_neurons), 'activation': 'tanh'},
                                     len(self.languages)])
