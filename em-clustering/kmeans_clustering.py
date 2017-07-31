import csv

from sklearn.cluster import KMeans

data = []
artists = []
years = []
with open('data/annotated_jazz_albums.csv', 'r') as csvfile:
  reader = csv.DictReader(csvfile)
  headers = reader.fieldnames[3:]
  for row in reader:
    artists.append(row['artist_album'])
    years.append(row['year'])
    data.append([int(row[key]) for key in headers])

clusters = KMeans(n_clusters=25).fit_predict(data)

with open('data/clustered_kmeans.csv', 'w') as csvfile:
  fieldnames = ['artist_album', 'year', 'cluster']
  writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

  writer.writeheader()

  for i, cluster in enumerate(clusters):
    writer.writerow({'artist_album': artists[i],
             'year': years[i],
             'cluster': cluster})
