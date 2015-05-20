import unittest
import io
import re
import xml.etree.ElementTree as ET

class TestHTMLEmail(unittest.TestCase):
  def setUp(self):
    self.html_file = './test/fixtures/html.eml'
    self.html = io.open(self.html_file, 'r').read()
    self.html_email = Email(html_file)

  def test_parses_stores_inner_text_html(self):
    body = html.split("\n\n")[1:].join("\n\n")
    expected = reduce(lambda a,b: a + b, ET.fromstring(body).itertext())
    self.assertEqual(self.html_email.body, expected)

  def test_stores_subject(self):
    subject = re.match("Subject: (.*)$", self.html).group(1)
    self.assertEqual(self.html_email.subject, subject)
