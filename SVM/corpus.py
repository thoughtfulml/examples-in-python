import re


class Corpus(object):
    skip_regex = re.compile(r'[\'"\.\?\!]+')
    space_regex = re.compile(r'\s', re.UNICODE)
    stop_words = [x.strip() for x in open('data/stopwords.txt').readlines()]
    sentiment_to_number = {'positive': 1, 'negative': -1}

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
    def sentiment_code(self):
        return self.sentiment_to_number[self._sentiment]

    def get_words(self):
        if self._words is None:
            self._words = set()
            for line in self._io:
                for word in Corpus.tokenize(line):
                    self._words.add(word)
            self._io.seek(0)
        return self._words

    def get_sentences(self):
        for line in self._io:
            yield line
