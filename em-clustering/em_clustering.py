from collections import namedtuple
import random
import logging
import math

import numpy as np
from numpy.linalg import LinAlgError


def dvmnorm(x, mean, covariance, log=False):
  """density function for the multivariate normal distribution
  based on sources of R library 'mvtnorm'
  :rtype : np.array
  :param x: vector or matrix of quantiles. If x is a matrix, each row is taken to be a quantile
  :param mean: mean vector, np.array
  :param covariance: covariance matrix, np.array
  :param log: if True, densities d are given as log(d), default is False
  """
  # TODO: add another methods from mvtnorm (calculate matrix square root using eigenvalues or SVD
  # TODO: add check for matching of input matrix dimensions
  n = covariance.shape[0]
  try:
    dec = np.linalg.cholesky(covariance)
  except LinAlgError:
    dec = np.linalg.cholesky(covariance + np.eye(covariance.shape[0]) * 0.0001)
  tmp = np.linalg.solve(dec, np.transpose(x - mean))
  rss = np.sum(tmp * tmp, axis=0)
  logretval = - np.sum(np.log(np.diag(dec))) - 0.5 * n * np.log(2 * math.pi) - 0.5 * rss
  if log:
    return logretval
  else:
    return np.exp(logretval)


class EMClustering(object):
  logger = logging.getLogger(__name__)
  ch = logging.StreamHandler()
  formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
  ch.setFormatter(formatter)
  logger.addHandler(ch)
  logger.setLevel(logging.DEBUG)

  cluster = namedtuple('cluster', 'weight, mean, covariance')

  def __init__(self, n_clusters):
    self._data = None
    self._clusters = None
    self._membership_weights = None
    self._partitions = None
    self._n_clusters = n_clusters

  @property
  def partitions(self):
    return self._partitions

  @property
  def data(self):
    return self._data

  @property
  def labels(self):
    return self._membership_weights

  @property
  def clusters(self):
    return self._clusters

  def fit_predict(self, data, iteration=5):
    self.setup(data)
    for i in range(iteration):
      self.logger.debug('Iteration %d', i)
      self.expect()
      self.maximize()
    return self

  def setup(self, data):
    self._n_samples, self._n_features = data.shape
    self._data = data
    self._membership_weights = np.ones((self._n_samples, self._n_clusters)) / self._n_clusters
    self._s = 0.2

    indices = list(range(data.shape[0]))
    random.shuffle(indices)
    pick_k_random_indices = random.sample(indices, self._n_clusters)

    self._clusters = []
    for cluster_num in range(self._n_clusters):
      mean = data[pick_k_random_indices[cluster_num], :]
      covariance = self._s * np.eye(self._n_features)
      self._clusters.append(self.cluster(1.0 / self._n_clusters, mean, covariance))

    self._partitions = np.empty(self._n_samples, dtype=np.int32)

  def expect(self):
    log_likelyhood = 0
    for cluster_num, cluster in enumerate(self._clusters):
      log_density = dvmnorm(self._data, cluster.mean, cluster.covariance, log=True)
      membership_weights = cluster.weight * np.exp(log_density)
      log_likelyhood += sum(log_density * self._membership_weights[:, cluster_num])

      self._membership_weights[:, cluster_num] = membership_weights

    for sample_num, probabilities in enumerate(self._membership_weights):
      prob_sum = sum(probabilities)

      self._partitions[sample_num] = np.argmax(probabilities)

      if prob_sum == 0:
        self._membership_weights[sample_num, :] = np.ones_like(probabilities) / self._n_clusters
      else:
        self._membership_weights[sample_num, :] = probabilities / prob_sum

    self.logger.debug('log likelyhood %f', log_likelyhood)

  def maximize(self):
    for cluster_num, cluster in enumerate(self._clusters):
      weights = self._membership_weights[:, cluster_num]

      weight = np.average(weights)
      mean = np.average(self._data, axis=0, weights=weights)
      covariance = np.cov(self._data, rowvar=False, ddof=0, aweights=weights)

      self._clusters[cluster_num] = self.cluster(weight, mean, covariance)
