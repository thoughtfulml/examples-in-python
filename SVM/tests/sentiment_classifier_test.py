from fractions import Fraction
import os
import unittest

from sentiment_classifier import SentimentClassifier


class TestSentimentClassifier(unittest.TestCase):
    def setUp(self):
        pass

    def validate(self, classifier, file, sentiment):
        total = 0
        misses = 0

        with(open(file, 'rb')) as f:
            for line in f:
                if classifier.classify(line) != sentiment:
                    misses += 1
                total += 1
        return Fraction(misses, total)

    def test_validate(self):
        """cross validates with an error of 35% or less"""
        neg = self.split_file('data/rt-polaritydata/rt-polarity.neg')
        pos = self.split_file('data/rt-polaritydata/rt-polarity.pos')

        classifier = SentimentClassifier.build([
            neg['training'],
            pos['training']
        ])

        c = 2 ** 7
        classifier.c = c

        n_er = self.validate(classifier, neg['validation'], 'negative')
        p_er = self.validate(classifier, pos['validation'], 'positive')
        total = Fraction(n_er.numerator + p_er.numerator,
                         n_er.denominator + p_er.denominator)
        print total
        self.assertLess(total, 0.35)

    def test_validate_itself(self):
        """yields a zero error when it uses itself"""
        classifier = SentimentClassifier.build([
            'data/rt-polaritydata/rt-polarity.neg',
            'data/rt-polaritydata/rt-polarity.pos'
        ])

        c = 2 ** 7
        classifier.c = c

        n_er = self.validate(classifier,
                             'data/rt-polaritydata/rt-polarity.neg',
                             'negative')
        p_er = self.validate(classifier,
                             'data/rt-polaritydata/rt-polarity.pos',
                             'positive')
        total = Fraction(n_er.numerator + p_er.numerator,
                         n_er.denominator + p_er.denominator)
        print total
        self.assertEqual(total, 0)

    def split_file(self, filepath):
        ext = os.path.splitext(filepath)[1]
        counter = 0
        training_filename = 'tests/fixtures/training%s' % ext
        validation_filename = 'tests/fixtures/validation%s' % ext
        with(open(filepath, 'rb')) as input_file:
            with(open(validation_filename, 'wb')) as val_file:
                with(open(training_filename, 'wb')) as train_file:
                    for line in input_file:
                        if counter % 2 == 0:
                            val_file.write(line)
                        else:
                            train_file.write(line)
                        counter += 1
        return {'training': training_filename,
                'validation': validation_filename}


'''
# encoding: utf-8
require_relative './spec_helper'

require 'minitest/mock'

describe SentimentClassifier do
  include TestMacros

  def validate(classifier, file, sentiment)
    total = 0
    misses = 0

    File.open(file, 'rb').each_line do |line|
      if classifier.classify(line) != sentiment
        misses += 1
      else
      end
      total += 1
    end

    Rational(misses, total)
  end

  it 'cross validates with an error of 35% or less' do
    neg = split_file("./config/rt-polaritydata/rt-polarity.neg")
    pos = split_file("./config/rt-polaritydata/rt-polarity.pos")

    classifier = SentimentClassifier.build([
      neg.fetch(:training),
      pos.fetch(:training)
    ])

    # find the minimum

    c = 2 ** 7
    classifier.c = c

    n_er = validate(classifier, neg.fetch(:validation), :negative)
    p_er = validate(classifier, pos.fetch(:validation), :positive)
    total = Rational(
      n_er.numerator + p_er.numerator,
      n_er.denominator + p_er.denominator
    )

    total.must_be :<, 0.35
  end

  it 'yields a zero error when it uses itself' do
    classifier = SentimentClassifier.build([
      "./config/rt-polaritydata/rt-polarity.neg",
      "./config/rt-polaritydata/rt-polarity.pos"
    ])

    c = 2 ** 7
    classifier.c = c

    n_er = validate(
      classifier,
      "./config/rt-polaritydata/rt-polarity.neg",
      :negative
    )

    p_er = validate(
      classifier,
      "./config/rt-polaritydata/rt-polarity.pos",
      :positive
    )

    total = Rational(
      n_er.numerator + p_er.numerator,
      n_er.denominator + p_er.denominator
    )

    total.must_equal 0.0
  end
end

require 'minitest/autorun'
require 'tempfile'
require 'mocha/setup'

Dir[File.expand_path('../../lib/**/*.rb', __FILE__)].each {|_| require _ }

module TestMacros
  def write_training_file(text, sentiment)
    file = Tempfile.new(sentiment)
    file.write(text)
    file.close
    file
  end

  def split_file(filepath)
    ext = File.extname(filepath)
    validation = File.open("./test/fixtures/validation#{ext}", "wb")
    training = File.open("./test/fixtures/training#{ext}", "wb")

    counter = 0
    File.open(filepath, 'rb').each_line do |l|
      if (counter) % 2 == 0
        validation.write(l)
      else
        training.write(l)
      end
      counter += 1
    end
    training.close
    validation.close

    {
      :training => training.path,
      :validation => validation.path
    }
  end
end
'''
