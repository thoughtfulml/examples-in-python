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

    def fit_predict(self, data, iteration=50):
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

        indices = range(data.shape[0])
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


'''
require 'matrix'
class EMClusterer
  attr_reader :partitions, :data, :labels, :clusters

  def initialize(k, data)
    @k = k
    @data = data
    setup_cluster!
  end

  def cluster(iterations = 5)
    iterations.times do |i|
      puts "Iteration #{i}"
      expect_maximize
    end
  end

  def good_enough?
    @labels.all? do |probabilities|
      probabilities.max > 0.9
    end
  end

  def expect_maximize
    expect
    maximize
  end

  def setup_cluster!
    @labels = Array.new(@data.row_size) { Array.new(@k) { 1.0 / @k }}

    @width = @data.column_size
    @s = 0.2

    pick_k_random_indices = @data.row_size.times.to_a.shuffle.sample(@k)

    @clusters = @k.times.map do |cc|
      {
        :means => @data.row(pick_k_random_indices.shift),
        :covariance => @s * Matrix.identity(@width)
      }
    end
    @partitions = []
  end

  def restart!
    puts "Restarting"
    setup_cluster!
    expect
  end

  def expect
    @clusters.each_with_index do |cluster, i|
      puts "Expectation for class #{i}"

      inv_cov = if cluster[:covariance].regular?
        cluster[:covariance].inv
      else
        puts "Applying shrinkage"
        (cluster[:covariance] - (0.0001 * Matrix.identity(@width))).inv
      end

      d = Math::sqrt(cluster[:covariance].det)

      @data.row_vectors.each_with_index do |row, j|
        rel = row - cluster[:means]

        p = d * Math::exp(-0.5 * fast_product(rel, inv_cov))
        @labels[j][i] = p
      end
    end

    @labels = @labels.map.each_with_index do |probabilities, i|
      sum = probabilities.inject(&:+)

      @partitions[i] = probabilities.index(probabilities.max)

      if sum.zero?
        probabilities.map { 1.0 / @k }
      else
        probabilities.map {|p| p / sum.to_f }
      end
    end
  end

  def fast_product(rel, inv_cov)
    sum = 0

    inv_cov.column_count.times do |j|
      local_sum = 0
      (0 ... rel.size).each do |k|
        local_sum += rel[k] * inv_cov[k, j]
      end
      sum += local_sum * rel[j]
    end

    sum
  end

  def maximize
    @clusters.each_with_index do |cluster, i|
      puts "Maximizing for class #{i}"
      sum = Array.new(@width) { 0 }
      num = 0

      @data.each_with_index do |row, j|
        p = @labels[j][i]

        @width.times do |k|
          sum[k] += p * @data[j,k]
        end

        num += p
      end

      mean = sum.map {|s| s / num }
      covariance = Matrix.zero(@width, @width)

      @data.row_vectors.each_with_index do |row, j|
        p = @labels[j][i]
        rel = row - Vector[*mean]
        covariance += Matrix.build(@width, @width) do |m,n|
          rel[m] * rel[n] * p
        end
      end

      covariance = (1.0 / num) * covariance

      @clusters[i][:means] = Vector[*mean]
      @clusters[i][:covariance] = covariance
    end
  end

  def to_s
    partitions
  end
end

# data = Matrix[
#   [1,1],
#   [1,2],
#   [1,3],
#   [2,1],
#   [3,1],
#   [3,2],
#   [3,3],
#   [4,1],
#   [5,1],
#   [5,2],
#   [5,3],
#   [6,4],
#   [6,5],
#   [6,6],
#   [6,7],
#   [6,8],
#   [7,4],
#   [7,6],
#   [7,8],
#   [8,4],
#   [8,6],
#   [8,8]
# ]
'''
