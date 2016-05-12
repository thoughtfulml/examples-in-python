import numpy as np
from scipy.sparse import csr_matrix, vstack
from corpus import Corpus


class CorpusSet(object):
    def __init__(self, corpora):
        self._yes = None
        self._xes = None
        self._calculated = False
        self._corpora = corpora
        self._words = set()
        for corpus in self._corpora:
            self._words.update(corpus.words)

    @property
    def words(self):
        return self._words

    def to_sparse_vectors(self):
        self._calculate_sparse_vectors()
        return self._yes, self._xes

    def _calculate_sparse_vectors(self):
        if self._calculated:
            return
        self._yes = []
        self._xes = None
        for corpus in self._corpora:
            vectors = self.load_corpus(corpus)
            if self._xes is None:
                self._xes = vectors
            else:
                self._xes = vstack((self._xes, vectors))
            self._yes.extend([corpus.sentiment_code] * vectors.shape[0])
        self._calculated = True

    def load_corpus(self, corpus):
        vectors = None
        for sentence in corpus.sentences:
            vector = self.sparse_vector(sentence)
            if vectors is None:
                vectors = vector
            else:
                vectors = vstack((vectors, vector))
        return vectors

    def sparse_vector(self, sentence):
        word_list = list(self._words)
        vector = csr_matrix((1, len(word_list)), dtype=np.float64)
        for token in Corpus.tokenize(sentence):
            if token in self._words:
                index = word_list.index(token)
                vector[0, index] = 1
        return vector


'''require 'libsvm'
class CorpusSet

  attr_reader :words

  def initialize(corpora)
    @corpora = corpora
    @words = corpora.reduce(Set.new) do |set, corpus|
      set.merge(corpus.words)
    end.to_a
  end

  def to_sparse_vectors
    calculate_sparse_vectors!
    [@yes, @xes]
  end

  def sparse_vector(string)
    vector = Hash.new(0)
    Corpus.tokenize(string).each do |token|
      vector[@words.to_a.index(token)] = 1
    end

    Libsvm::Node.features(vector)
  end

  private
  def calculate_sparse_vectors!
    return if @state == :calculated
    @yes = []
    @xes = []
    @corpora.each do |corpus|
      vectors = load_corpus(corpus)
      @xes.concat(vectors)
      @yes.concat([corpus.sentiment_code] * vectors.length)
    end
    @state = :calculated
  end

  def load_corpus(corpus)
    vectors = []
    corpus.sentences do |sentence|
      vectors << sparse_vector(sentence)
    end
    vectors
  end
end
'''
