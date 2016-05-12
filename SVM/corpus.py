import re


class Corpus(object):
    skip_regex = re.compile(r'[\'"\.\?\!]+')
    space_regex = re.compile(r'\s', re.UNICODE)
    stop_words = [x.strip() for x in open('data/stopwords.txt').readlines()]

    @classmethod
    def tokenize(cls, text):
        cleared_text = cls.skip_regex.sub('', text)
        parts = cls.space_regex.split(cleared_text)
        parts = [part.lower() for part in parts]
        return [part for part in parts if len(part) > 0 and part not in cls.stop_words]

    def __init__(self, io, sentiment):
        self._io = io
        self._sentiment = sentiment
        self._words = None

    @property
    def sentiment(self):
        return self._sentiment

    @property
    def words(self):
        if self._words is None:
            self._words = set()
            for line in self._io:
                for word in Corpus.tokenize(line):
                    self._words.add(word)
            self._io.seek(0)
        return self._words

    @property
    def sentences(self):
        for line in self._io:
            yield line

    @property
    def sentiment_code(self):
        return {'positive': 1, 'negative': -1}[self._sentiment]


'''
require 'libsvm'
require 'set'

class Corpus
  STOPWORDS = File.read(
    File.expand_path("../../config/stopwords.txt", __FILE__)
  ).split("\n").map(&:strip)

  STOP_SYMBOL = %w[. ? ! ' "].concat([' ', "\u00A0"])

  attr_reader :sentiment

  def initialize(io, sentiment)
    @io = io
    @sentiment = sentiment
  end

  def sentences(&block)
    @io.each_line do |line|
      yield line
    end
    @io.rewind
  end

  def sentiment_code
    {
      :positive => 1,
      :negative => -1
    }.fetch(@sentiment)
  end

  def self.tokenize(string)
    string.downcase.gsub(/['"\.\?\!]/, '').split(/[[:space:]]/).select do |w|
      !STOPWORDS.include?(w)
    end
  end

  def words
    @words ||= begin
      set = Set.new
      @io.each_line do |line|
        Corpus.tokenize(line).each do |word|
          set << word
        end
      end
      @io.rewind
      set
    end
  end
end
'''
