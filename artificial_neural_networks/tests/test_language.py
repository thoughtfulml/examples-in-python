# coding=utf-8
from io import StringIO
import string
import unittest

from artificial_neural_networks.language import Language


class TestLanguage(unittest.TestCase):
    def setUp(self):
        self.language_data = u'''
abcdefghijklmnopqrstuvwxyz.
ABCDEFGHIJKLMNOPQRSTUVWXYZ.
\u00A0.
!~@#$%^&*()_+'?[]“”‘’—<>»«›‹–„/.
ïëéüòèöÄÖßÜøæåÅØóąłżŻśęńŚćźŁ.
'''
        self.special_characters = self.language_data.split("\n")[-1].strip()
        self.language_io = StringIO(self.language_data)
        self.language = Language(self.language_io, 'English')

    def test_keys(self):
        """has the proper keys for each vector"""
        self.assertListEqual(list(string.ascii_lowercase),
                             sorted(self.language.vectors[0].keys()))
        self.assertListEqual(list(string.ascii_lowercase),
                             sorted(self.language.vectors[1].keys()))

        special_chars = sorted(set(u'ïëéüòèöäößüøæååóąłżżśęńśćź'))
        self.assertListEqual(special_chars,
                             sorted(self.language.vectors[-1].keys()))

    def test_values(self):
        """sums to 1 for all vectors"""
        for vector in self.language.vectors:
            self.assertEqual(1, sum(vector.values()))

    def test_character_set(self):
        """returns characters that is a unique set of characters used"""
        chars = list(string.ascii_lowercase)
        chars += list(set(u'ïëéüòèöäößüøæååóąłżżśęńśćź'))

        self.assertListEqual(sorted(chars),
                             sorted(self.language.characters))
