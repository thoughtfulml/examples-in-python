import unittest

import io
import re
from email_object import EmailObject


class TestPlaintextEmailObject(unittest.TestCase):
  CLRF = "\n\n"

  def setUp(self):
    self.plain_file = './tests/fixtures/plain.eml'
    with io.open(self.plain_file, 'rb') as plaintext:
      self.text = plaintext.read().decode('utf-8')
      plaintext.seek(0)
      self.plain_email = EmailObject(plaintext)

  def test_parse_plain_body(self):
    body = self.CLRF.join(self.text.split(self.CLRF)[1:])
    self.assertEqual(self.plain_email.body(), body)

  def test_parses_the_subject(self):
    subject = re.search("Subject: (.*)", self.text).group(1)
    self.assertEqual(self.plain_email.subject(), subject)
