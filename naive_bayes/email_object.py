import email

from bs4 import BeautifulSoup


class EmailObject:
    CLRF = "\n\r\n\r"

    def __init__(self, file, category=None):
        self.file = file
        self.category = category
        self.mail = email.message_from_file(self.file)
        self.file.close()

    def subject(self):
        return self.mail.get('Subject')

    def body(self):
        payload = self.mail.get_payload()
        if self.mail.is_multipart():
            parts = [self.single_body(part) for part in list(payload)]
        else:
            parts = [self.single_body(self.mail)]
        parts = [part for part in parts if len(part) > 0]
        return self.CLRF.join(parts)

    def single_body(self, part):
        content_type = part.get_content_type()
        try:
            body = part.get_payload(decode=True)
            body = body.decode(errors='replace')
        except:
            return ''

        # if isinstance(body, bytes):
        #     if part.get_content_charset() is None or part.get_content_charset() == 'default':
        #         encoding = 'us-ascii'
        #     else:
        #         encoding = part.get_content_charset()
        # body = body.decode(encoding=encoding, errors='replace')

        if content_type == 'text/html':
            return BeautifulSoup(body, 'html.parser').text
        elif content_type == 'text/plain':
            return body
        else:
            return ''
