import csv
import unittest

import numpy as np

from em_clustering import EMClustering


class TestEMClustering(unittest.TestCase):
    def test_with_old_faithful(self):
        """test based on well known example - investigation of dependencies between eruption time
        and wait time of Old Faithful geyser and on code from https://commons.wikimedia.org/wiki/File:Em_old_faithful.gif"""

        data = []

        with open('tests/old_faithful.csv', 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            headers = reader.fieldnames[1:]
            for row in reader:
                data.append([float(row[key]) for key in headers])

        clustering = EMClustering(n_clusters=2)

        data = np.array(data)

        clustering._n_samples, clustering._n_features = data.shape
        clustering._data = data
        clustering._membership_weights = np.ones(
            (clustering._n_samples, clustering._n_clusters)) / clustering._n_clusters
        clustering._s = 0.2

        clustering._clusters = [
            clustering.cluster(0.5, np.array([2.8, 75]), np.array([[0.8, 7], [7, 70]])),
            clustering.cluster(0.5, np.array([3.6, 58]), np.array([[0.8, 7], [7, 70]]))
        ]

        clustering._partitions = np.empty(clustering._n_samples, dtype=np.int32)

        for i in range(30):
            clustering.expect()
            clustering.maximize()

        # test against execution of R code
        self.assertAlmostEqual(0.64, clustering._clusters[0].weight, places=2)
        self.assertAlmostEqual(4.29, clustering._clusters[0].mean[0], places=2)
        self.assertAlmostEqual(79.97, clustering._clusters[0].mean[1], places=2)
        self.assertAlmostEqual(0.36, clustering._clusters[1].weight, places=2)
        self.assertAlmostEqual(2.04, clustering._clusters[1].mean[0], places=2)
        self.assertAlmostEqual(54.48, clustering._clusters[1].mean[1], places=2)
