import collections
from copy import copy


class CorpusParser:
    NULL_CHARACTER = 'START'
    STOP = ' \n'
    SPLITTER = '/'

    def __init__(self):
        self.ngram = 2

    TagWord = collections.namedtuple('TagWord', ['word', 'tag'])

    def parse(self, stream):
        ngrams = self.ngram * [CorpusParser.TagWord(CorpusParser.NULL_CHARACTER,
                                                    CorpusParser.NULL_CHARACTER)]
        word = ''
        pos = ''
        parse_word = True

        for char in stream:
            if char == '\t' or (len(word) == 0 and char in CorpusParser.STOP):
                continue
            elif char == CorpusParser.SPLITTER:
                parse_word = False
            elif char in CorpusParser.STOP:
                ngrams.pop(0)
                ngrams.append(CorpusParser.TagWord(word, pos))

                yield copy(ngrams)

                word = ''
                pos = ''
                parse_word = True
            elif parse_word:
                word += char
            else:
                pos += char

        if len(word) > 0 and len(pos) > 0:
            ngrams.pop(0)
            ngrams.append(CorpusParser.TagWord(word, pos))
            yield copy(ngrams)
