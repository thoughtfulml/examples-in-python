import unittest

describe Tokenizer do
  let(:string) { "this is a test of the emergency broadcasting system" }

  describe '1-gram tokenization' do
    it 'downcases all words' do
      expectation = %w[this is all caps]
      Tokenizer.tokenize('THIS IS ALL CAPS') do |token|
        expected_token = expectation.shift

        token.must_equal expected_token
      end
    end

    it 'tokenizes a wone word sentence' do
      Tokenizer.tokenize('quick') do |token|
        token.must_equal 'quick'
      end
    end
  end

  describe 'ngrams' do
    it 'builds the proper ngrams' do
      expectation = [
        ["\u0000", "quick"],
        ["quick", "brown"],
        ["brown", "fox"],
      ]

      Tokenizer.ngram("quick brown fox", 2) do |gram|
        gram.must_equal expectation.shift
      end
    end

    it 'uses the block if given' do
      Tokenizer.ngram("quick", 2) do |ngram|
        ngram.must_equal ["\u0000", "quick"]
      end
    end

    it 'will build a cumulative lookback ngram array' do
      expectation = [
        ["\u0000", "the"],
        ["the"],
        ["the", "quick"],
        ["quick"],
        ["quick", "brown"],
        ["brown"],
        ["brown", "fox"],
        ["fox"]
      ]
      Tokenizer.cumulative_ngram("the quick brown fox", 2) do |gram|
        gram.must_equal expectation.shift
      end
    end

    it 'pads the first gram with n-1 \u0000' do
      first_ngram = nil

      Tokenizer.ngram(string, 3) do |gram|
        first_ngram = gram
        break
      end

      first_ngram.first(2).must_equal ["\u0000", "\u0000"]
    end
  end
end
