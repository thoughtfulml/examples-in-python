import csv

import numpy as np

from em_clustering import EMClustering

np.set_printoptions(threshold=9000)

data = []
artists = []
years = []

# with open('data/less_covariance_jazz_albums.csv', 'rb') as csvfile:
with open('data/annotated_jazz_albums.csv', 'r') as csvfile:
  reader = csv.DictReader(csvfile)
  headers = reader.fieldnames[3:]
  for row in reader:
    artists.append(row['artist_album'])
    years.append(row['year'])
    data.append([int(row[key]) for key in headers])

clusterer = EMClustering(n_clusters=25)
clusters = clusterer.fit_predict(np.array(data))

print(clusters.partitions)
