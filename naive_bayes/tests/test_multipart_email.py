import unittest

import io
import re
from email_object import EmailObject


class TestMultipartEmailObject(unittest.TestCase):
  def setUp(self):
    self.multipart_file = './tests/fixtures/multipart.eml'
    with io.open(self.multipart_file, 'rb') as multipart:
      self.text = multipart.read().decode('utf-8')
      multipart.seek(0)
      self.multipart_email = EmailObject(multipart)

  def test_parse_concatenated_body_of_text(self):
    internal_mail = self.multipart_email.mail
    assert internal_mail.is_multipart()

    body = b''
    for part in internal_mail.walk():
      if re.match("text/plain", part.get_content_type()):
        body += part.get_payload(decode=True)
      elif re.match("text/html", part.get_content_type()):
        body += part.get_payload(decode=True)
    body = body.decode()
    self.assertEqual(self.multipart_email.body(), body)

  def test_stores_subject(self):
    subject = re.search("Subject: (.*)", self.text).group(1)
    self.assertEqual(self.multipart_email.subject(), subject)
