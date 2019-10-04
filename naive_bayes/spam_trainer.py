"""
Chapter 4. Naive Bayesian Classification
SpamTrainer class
"""
from collections import defaultdict
from email_object import EmailObject
from tokenizer import Tokenizer
import io
import math
import numpy as np


class SpamTrainer(object):
    """
  Storing training data
  Building a Bayesian classifier
  Error minimization through cross-validation
  """

    class Classification(object):
        """
    Guess and score
    """

        def __init__(self, guess, score):
            self.guess = guess
            self.score = score

        def __eq__(self, other):
            return self.guess == other.guess and self.score == other.score

    def __init__(self, training_files):
        self.categories = set()

        for category, _ in training_files:
            self.categories.add(category)

        self.totals = defaultdict(float)

        self.training = {c: defaultdict(float) for c in self.categories}

        self.to_train = training_files

        self.class_log_prior = {}
        self.B = 0

    def normalized_score(self, email):
        """
    Calculates normalized score
    :param email: EmailObject
    :return: float number
    """
        score = self.score(email)
        scoresum = sum(score.values())

        normalized = {cat: (aggregate / scoresum) for cat, aggregate in score.items()}
        return normalized

    def total_for(self, category):
        """
    Get
    :param category:
    :return:
    """
        return self.totals[category]

    def train(self):
        y = []
        for category, file in self.to_train:
            with io.open(file, "rb") as eml_file:
                email = EmailObject(eml_file)

            self.categories.add(category)
            y.append(1 if category == "spam" else 0)

            for token in Tokenizer.unique_tokenizer(email.body()):
                self.training[category][token] += 1
                self.totals["_all"] += 1
                self.totals[category] += 1

        if self.to_train:
            y = np.array(y)
            self.class_log_prior["spam"] = math.log(sum(y == 1) / y.shape[0])
            self.class_log_prior["ham"] = math.log(sum(y == 0) / y.shape[0])
            self.B = len(
                set(self.training["spam"].keys()).union(
                    set(self.training["ham"].keys())
                )
            )
            self.to_train = {}

    def score(self, email):
        """
    Calculates score
    :param email: EmailObject
    :return: float number
    """
        self.train()

        cat_totals = self.totals

        aggregates = {cat: self.class_log_prior[cat] for cat in self.categories}

        for token in Tokenizer.unique_tokenizer(email.body()):
            for cat in self.categories:
                value = self.training[cat][token]
                r = math.log((value + 1) / (cat_totals[cat] + self.B))
                aggregates[cat] += r
        max_val = (
            aggregates["spam"]
            if aggregates["spam"] > aggregates["ham"]
            else aggregates["ham"]
        )
        aggregates["spam"] = math.exp(aggregates["spam"] - max_val)
        aggregates["ham"] = math.exp(aggregates["ham"] - max_val)
        norm_factor = aggregates["spam"] + aggregates["ham"]
        aggregates["spam"] /= norm_factor
        aggregates["ham"] /= norm_factor
        return aggregates

    def preference(self):
        return sorted(self.categories, key=lambda cat: self.total_for(cat))

    def classify(self, email):
        score = self.score(email)

        max_score = 0.0
        preference = self.preference()
        max_key = preference[-1]

        for k, v in score.items():
            if v > max_score:
                max_key = k
                max_score = v
            elif v == max_score and preference.index(k) > preference.index(max_key):
                max_key = k
                max_score = v
        return self.Classification(max_key, max_score)
