import unittest
import io
import re

class TestPlaintextEmail(unittest.TestCase):
  def setUp(self):
    self.plain_file = './test/fixtures/plain.eml'
    self.plaintext = io.open(self.plain_file, 'r').read()
    self.plain_email = Email(plain_file)

  def test_parse_plain_body(self):
    body = self.plaintext.split("\n\n")[1:].join("\n\n")
    self.assertEqual(plain_email.body, body)

  def test_parses_the_subject(self):
    subject = re.match("Subject: (.*)$", self.plaintext).group(1)
    self.assertEqual(plain_email.subject, subject)
