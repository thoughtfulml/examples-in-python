import unittest
import io
import re
from BeautifulSoup import BeautifulSoup
from naive_bayes.email_object import EmailObject

class TestHTMLEmail(unittest.TestCase):
  def setUp(self):
    self.html_file = io.open('./tests/fixtures/html.eml', 'rb')
    self.html = self.html_file.read()
    self.html_file.seek(0)
    self.html_email = EmailObject(self.html_file)

  def test_parses_stores_inner_text_html(self):
    body = "\n\n".join(self.html.split("\n\n")[1:])
    expected = BeautifulSoup(body).text 
    self.assertEqual(self.html_email.body(), expected)


  def test_stores_subject(self):
    subject = re.search("Subject: (.*)", self.html).group(1)
    self.assertEqual(self.html_email.subject(), subject)
