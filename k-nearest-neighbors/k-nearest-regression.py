from pandas import Series, DataFrame
import pandas as pd
import numpy as np
import numpy.random as npr
from scipy.spatial import KDTree

class KNearestNeighbor:
  def __init__(self, csv_file):
    self.df = pd.read_csv(csv_file)
    self.n = len(self.df)

    self.outcomes = self.df['outcome']
    self.values = self.df['AppraisedValue']

    self.df = self.df.drop('outcomes', 1)
    self.df = self.df.drop('AppraisedValue', 1)

#define function
def kNN(X,y,k):
    #number of observations
    n = len(y)
    #Set up return values
    y_star = Series(np.zeros(n),dtype='Int64')
    #distance vector
    dist = squareform(pdist(X,metric='Euclidean'))
    #so it can't choose itself as a closest neighbour
    np.fill_diagonal(dist,1e10)
    #Loop through each observation
    for i in range(n):
    #Find the y values of the k nearest neighbours
    y_nearest = y[dist[i,:].argsort()[:k]]
    #assign y_hat
    if y_nearest.mean()> 0.5:
        y_hat[i] = 1
    #return the predicted classification
    return y_hat

  total = 0
  count = 0
  for ti in testing_idxs:
    response = kd.query(df.iloc[ti])
    actual = values[ti]
    expected = values[training_idxs[response[-1]]]
    print count
    total += abs(actual - expected)
    count += 1
