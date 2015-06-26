from pandas import Series, DataFrame
import pandas as pd
import numpy as np
import numpy.random as npr
import random
from scipy.spatial import KDTree
from sklearn.metrics import mean_absolute_error
import sys

sys.setrecursionlimit(10000)

class Regression:
  def __init__(self, csv_file = None, data = None, values = None):
    if (data is None and csv_file is not None):
      df = pd.read_csv(csv_file)
      self.values = df['AppraisedValue']
      df = df.drop('AppraisedValue', 1)
      df = (df - df.mean()) / (df.max() - df.min())
      self.df = df
      self.df = self.df[['lat', 'long', 'SqFtLot']]
   
    elif (data is not None and values is not None):
      self.df = data
      self.values = values
    else:
      raise ValueError("Must have either csv_file or data set")

    self.n = len(self.df)

    self.kdtree = KDTree(self.df)
    self.metric = np.mean
    self.k = 5

  def regress(self, query_point):
    distances, indexes = self.kdtree.query(query_point, self.k)
    m = self.metric(self.values.iloc[indexes])
    if np.isnan(m):
      zomg
    else:
      return m

  def error_rate(self, folds):
    holdout = 1 / float(folds)
    errors = []
    for fold in range(folds):
      y_hat, y_true = self.__validation_data(holdout)
      errors.append(mean_absolute_error(y_true, y_hat))

    return errors
    

  def __validation_data(self, holdout):
    test_rows = random.sample(self.df.index, int(round(len(self.df) * holdout)))
    train_rows = set(range(len(self.df))) - set(test_rows)
    df_test = self.df.ix[test_rows]
    df_train = self.df.drop(test_rows)
    
    test_values = self.values.ix[test_rows]
    train_values = self.values.ix[train_rows] 
    kd = Regression(data=df_train, values=train_values) 

    y_hat = []
    y_actual = []

    for idx, row in df_test.iterrows():
      y_hat.append(kd.regress(row))
      y_actual.append(self.values[idx])

    return (y_hat, y_actual)
