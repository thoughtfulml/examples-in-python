from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from numpy.random import permutation
from numpy import array_split, concatenate
import pandas as pd
import numpy as np

class MushroomClassifier:
  def __init__(self, data_file):
    self.dataFrame = pd.read_csv(data_file)
    for k in self.dataFrame.columns[1:]:
      self.dataFrame[k], _ = pd.factorize(self.dataFrame[k])

    self.classes = np.array(sorted(pd.Categorical(self.dataFrame['class']).categories))
    self.features = self.dataFrame.columns[self.dataFrame.columns != 'class']

  def validate(self, folds):
    confusion_matrices = []

    df = self.dataFrame

    assert len(df) > folds

    perms = array_split(permutation(len(df)), folds)

    for i in range(folds):
      train_idxs = range(folds)
      train_idxs.pop(i)
      train = []
      for idx in train_idxs:
        train.append(perms[idx])

      train = concatenate(train)

      test_idx = perms[i]

      training = df.iloc[train]
      test_data = df.iloc[test_idx]

      confusion_matrices.append(self.confusion_matrix(training, test_data))

    return confusion_matrices

  def confusion_matrix(self, train, test):
    y, _ = pd.factorize(pd.Categorical(train['class']), sort=True)

    classifier = self.train(train[self.features], y)
    predictions = self.classes[classifier.predict(test[self.features])]

    return pd.crosstab(test['class'], predictions, rownames=['actual'], colnames=['preds'])

class MushroomForest(MushroomClassifier):
  def train(self, X, Y):
    clf = RandomForestClassifier(n_jobs = 2)
    clf = clf.fit(X, Y)
    self.classifier = clf
    return clf

class MushroomTree(MushroomClassifier):
  def train(self, X, Y):
    clf = DecisionTreeClassifier()
    clf = clf.fit(X, Y)
    self.classifier = clf
    return clf
