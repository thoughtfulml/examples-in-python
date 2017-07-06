import numpy as np
from scipy.sparse import csr_matrix, vstack

from .corpus import Corpus


class CorpusSet(object):
    def __init__(self, corpora):
        self._yes = None
        self._xes = None
        self._corpora = corpora
        self._words = set()
        for corpus in self._corpora:
            self._words.update(corpus.get_words())

    @property
    def words(self):
        return self._words

    @property
    def xes(self):
        return self._xes

    @property
    def yes(self):
        return self._yes

    def calculate_sparse_vectors(self):
        self._yes = []
        self._xes = None
        for corpus in self._corpora:
            vectors = self.feature_matrix(corpus)
            if self._xes is None:
                self._xes = vectors
            else:
                self._xes = vstack((self._xes, vectors))
            self._yes.extend([corpus.sentiment_code] * vectors.shape[0])

    def feature_matrix(self, corpus):
        data = []
        indices = []
        indptr = [0]
        for sentence in corpus.get_sentences():
            sentence_indices = self._get_indices(sentence)
            indices.extend(sentence_indices)
            data.extend([1] * len(sentence_indices))
            indptr.append(len(indices))
        feature_matrix = csr_matrix((data, indices, indptr),
                                    shape=(len(indptr) - 1,
                                           len(self._words)),
                                    dtype=np.float64)
        feature_matrix.sort_indices()
        return feature_matrix

    def feature_vector(self, sentence):
        indices = self._get_indices(sentence)
        data = [1] * len(indices)
        indptr = [0, len(indices)]
        vector = csr_matrix((data, indices, indptr),
                            shape=(1, len(self._words)),
                            dtype=np.float64)
        return vector

    def _get_indices(self, sentence):
        word_list = list(self._words)
        indices = []
        for token in Corpus.tokenize(sentence):
            if token in self._words:
                index = word_list.index(token)
                indices.append(index)
        return indices
