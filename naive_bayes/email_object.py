"""
Chapter 4. Naive Bayesian Classification
EmailObject class
"""
import email
import sys

from bs4 import BeautifulSoup


class EmailObject(object):
    """
    Parses incoming email messages
    """
    CLRF = "\n\r\n\r"

    def __init__(self, infile, category=None):
        self.category = category
        if sys.version_info > (3, 0):
            # Python 3 code in this block
            self.mail = email.message_from_binary_file(infile)
        else:
            # Python 2 code in this block
            self.mail = email.message_from_file(infile)

    def subject(self):
        """
        Get message subject line
        :return: str
        """
        return self.mail.get('Subject')

    def body(self):
        """
        Get message body
        :return: str in Py3, unicode in Py2
        """
        payload = self.mail.get_payload()
        if self.mail.is_multipart():
            parts = [self._single_body(part) for part in list(payload)]
        else:
            parts = [self._single_body(self.mail)]
        parts = [part for part in parts if len(part) > 0]
        return self.CLRF.join(parts)

    @staticmethod
    def _single_body(part):
        """
        Get text from part.
        :param part: email.Message
        :return: str body or empty str if body cannot be decoded
        """
        content_type = part.get_content_type()
        try:
            body = part.get_payload(decode=True)
            # body = body.decode(errors='replace')
        except Exception:
            return ''

        if content_type == 'text/html':
            return BeautifulSoup(body, 'html.parser').text
        elif content_type == 'text/plain':
            return body
        return ''
