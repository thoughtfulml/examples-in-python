import unittest
import sys

import re
from bs4 import BeautifulSoup
from naive_bayes.email_object import EmailObject


class TestHTMLEmail(unittest.TestCase):
    def setUp(self):
        self.html_file = open('./tests/fixtures/html.eml', 'r')
        self.html = self.html_file.read()
        self.html_file.seek(0)
        self.html_email = EmailObject(self.html_file)

    def test_parses_stores_inner_text_html(self):
        body = "\n\n".join(self.html.split("\n\n")[1:])
        if sys.version_info > (3, 0):
            # Python 3 code in this block
            expected = BeautifulSoup(body, 'html.parser').text.encode('raw-unicode-escape').decode('iso-8859-1')
        else:
            # Python 2 code in this block
            expected = BeautifulSoup(body, 'html.parser', from_encoding="iso-8859-1").text
        self.assertEqual(self.html_email.body(), expected)

    def test_stores_subject(self):
        subject = re.search("Subject: (.*)", self.html).group(1)
        self.assertEqual(self.html_email.subject(), subject)
