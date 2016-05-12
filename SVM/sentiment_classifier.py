import os
from numpy import ndarray

from sklearn import svm

from corpus import Corpus
from corpus_set import CorpusSet


class SentimentClassifier(object):
    ext_to_sentiment = {'.pos': 'positive',
                        '.neg': 'negative'}

    number_to_sentiment = {-1: 'negative',
                           1: 'positive'}

    @classmethod
    def present_answer(cls, answer):
        if isinstance(answer, ndarray):
            answer = answer[0]
        return cls.number_to_sentiment[answer]

    @classmethod
    def build(cls, files):
        corpora = []
        for file in files:
            ext = os.path.splitext(file)[1]
            corpus = Corpus(open(file, 'rb'),
                            cls.ext_to_sentiment[ext])
            corpora.append(corpus)
        corpus_set = CorpusSet(corpora)
        return SentimentClassifier(corpus_set)

    def __init__(self, corpus_set):
        self._trained = False
        self._corpus_set = corpus_set
        self._c = 2 ** 7
        self._model = None

    @property
    def c(self):
        return self._c

    @c.setter
    def c(self, cc):
        self._c = cc
        self._model = None

    def words(self):
        return self._corpus_set.words

    def classify(self, string):
        if self._model is None:
            self._model = self.model()
        prediction = self._model.predict(self._corpus_set.sparse_vector(string))
        return self.present_answer(prediction)

    def model(self):
        y_vec, x_mat = self._corpus_set.to_sparse_vectors()
        clf = svm.SVC(C=self.c,
                      cache_size=1000,
                      gamma=1.0 / len(y_vec),
                      kernel='linear',
                      tol=0.001)
        clf.fit(x_mat, y_vec)
        return clf


'''
class SentimentClassifier
  def initialize(corpus_set)
    @corpus_set = corpus_set
    @c = 2 ** 7
  end

  def c=(cc)
    @c = cc
    @model = nil
  end

  def words
    @corpus_set.words
  end

  def self.build(files)
    new(CorpusSet.new(files.map do |file|
      mapping = {
        '.pos' => :positive,
        '.neg' => :negative
      }
      Corpus.new(File.open(file, 'rb'), mapping.fetch(File.extname(file)))
    end))
  end

  def present_answer(answer)
    {
      -1.0 => :negative,
      1.0 => :positive
    }.fetch(answer)
  end

  def classify(string)
    if trained?
      prediction = @model.predict(@corpus_set.sparse_vector(string))
      present_answer(prediction)
    else
      @model = model
      classify(string)
    end
  end

  def trained?
    !!@model
  end

  def model
    puts 'starting to get sparse vectors'
    y_vec, x_mat = @corpus_set.to_sparse_vectors

    prob = Libsvm::Problem.new
    parameter = Libsvm::SvmParameter.new
    parameter.cache_size = 1000

    parameter.gamma = Rational(1, y_vec.length).to_f
    parameter.eps = 0.001

    parameter.c = @c
    parameter.kernel_type = Libsvm::KernelType::LINEAR

    prob.set_examples(y_vec, x_mat)
    Libsvm::Model.train(prob, parameter)
  end
end
'''
