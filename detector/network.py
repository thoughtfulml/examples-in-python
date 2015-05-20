from pybrain.tools.shortcuts import buildNetwork
from pybrain.datasets import SupervisedDataSet
from pybrain.supervised.trainers import RPropMinusTrainer, BackpropTrainer
import numpy as np

class Network:
  def __init__(self, languages, error=0.005):
    self.languages = languages
    self.inputs = set()
    for l in languages:
      self.inputs = self.inputs.union(l.characters)

    self.error = error

  def run(self, sentence):
    vectors, characters = Tokenizer.tokenize(sentence)
    output_vector = self.net.activate(code(vectors[0]))
    return self.languages[output_vector.index(max(output_vector)]

  def buildTrainer(self):
    inputLength = len(self.inputs)
    outputLength = len(self.languages)
    hiddenNeurons = (2 * (inputLength + outputLength)) / 3

    self.net = buildNetwork(inputLength, hiddenNeurons, outputLength) 

    self.dataSet = SupervisedDataSet(inputLength, outputLength)

    for idx, lang in enumerate(self.languages):
      outputVector = np.zeros(outputLength, dtype='int64')
      outputVector[idx] = 1

      for vector in lang.vectors:
        self.dataSet.addSample(self.code(vector), outputVector)

  def code(self, vector):
    if not vector:
      return []

    return list(vector.get(i, 0.0) for i in self.inputs)

  def train(self):
    self.buildTrainer()
    self.trainer = BackpropTrainer(self.net, dataset=self.dataSet)
