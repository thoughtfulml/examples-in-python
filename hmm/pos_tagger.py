from collections import defaultdict
import re

from corpus_parser import CorpusParser


class POSTagger:
    class LazyFile:
        def __init__(self, filename):
            self.filename = filename
            self.file = None

        def __iter__(self):
            self.file = open(self.filename, 'r')
            return self

        def next(self):
            try:
                line = self.file.next()
            except StopIteration, e:
                self.file.close()
                raise e
            return line

    @classmethod
    def from_filepaths(cls, training_files, eager=False):
        lazy_files = [POSTagger.LazyFile(fn) for fn in training_files]
        return POSTagger(lazy_files, eager)

    def __init__(self, data_io=(), eager=False):
        self.corpus_parser = CorpusParser()
        self.data_io = data_io
        self.trained = False
        if eager:
            self.train()
            self.trained = True

    def train(self):
        if not self.trained:
            self.tags = set()
            self.tag_combos = defaultdict(int)
            self.tag_frequencies = defaultdict(int)
            self.word_tag_combos = defaultdict(int)

            for io in self.data_io:
                for line in io:
                    for ngram in self.corpus_parser.parse(line):
                        self.write(ngram)
            self.trained = True

    def write(self, ngram):
        if ngram[0].tag == 'START':
            self.tag_frequencies['START'] += 1
            self.word_tag_combos['START/START'] += 1

        self.tags.add(ngram[-1].tag)

        self.tag_frequencies[ngram[-1].tag] += 1
        combo = ngram[-1].word + '/' + ngram[-1].tag
        self.word_tag_combos[combo] += 1
        combo = ngram[0].tag + '/' + ngram[-1].tag
        self.tag_combos[combo] += 1

    def viterbi(self, sentence):
        sentence1 = re.sub(r'([\.\?!])', r' \1', sentence)
        parts = re.split(r'\s+', sentence1)
        last_viterbi = {}
        backpointers = ['START']

        for tag in self.tags:
            if tag == 'START':
                continue
            else:
                probability = self.tag_probability('START', tag) \
                              * self.word_tag_probability(parts[0], tag)

                if probability > 0:
                    last_viterbi[tag] = probability

        if len(last_viterbi) > 0:
            backpointer = max(last_viterbi.iterkeys(),
                              key=(lambda key: last_viterbi[key]))
        else:
            backpointer = max(self.tag_frequencies.iterkeys(),
                              key=(lambda key: self.tag_frequencies[key]))
        backpointers.append(backpointer)

        for part in parts[1:]:
            viterbi = {}
            for tag in self.tags:
                if tag == 'START':
                    continue
                if len(last_viterbi) == 0:
                    break

                best_tag = max(last_viterbi.iterkeys(),
                               key=(lambda prev_tag: last_viterbi[prev_tag] *
                                                     self.tag_probability(prev_tag, tag) *
                                                     self.word_tag_probability(part, tag)))

                probability = last_viterbi[best_tag] * \
                              self.tag_probability(best_tag, tag) * \
                              self.word_tag_probability(part, tag)

                if probability > 0:
                    viterbi[tag] = probability

            last_viterbi = viterbi

            if len(last_viterbi) > 0:
                backpointer = max(last_viterbi.iterkeys(),
                                  key=(lambda key: last_viterbi[key]))
            else:
                backpointer = max(self.tag_frequencies.iterkeys(),
                                  key=(lambda key: self.tag_frequencies[key]))
            backpointers.append(backpointer)

        return backpointers

    def tag_probability(self, previous_tag, current_tag):
        """Maximum likelihood estimate
        count(previous_tag, current_tag) / count(previous_tag)"""
        denom = self.tag_frequencies[previous_tag]

        if denom == 0:
            return 0
        else:
            return self.tag_combos[previous_tag + '/' + current_tag] / float(denom)

    def word_tag_probability(self, word, tag):
        """Maximum Likelihood estimate
        count (word and tag) / count(tag)"""
        denom = self.tag_frequencies[tag]
        if denom == 0:
            return 0
        else:
            return self.word_tag_combos[word + '/' + tag] / float(denom)

    def probability_of_word_tag(self, words, tags):
        if len(words) != len(tags):
            raise ValueError('The word and tags must be the same length!')

        length = len(words)

        probability = 1.0

        for i in xrange(1, length):
            probability *= self.tag_probability(tags[i - 1], tags[i]) * \
                           self.word_tag_probability(words[i], tags[i])

        return probability
