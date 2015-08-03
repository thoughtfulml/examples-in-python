import email
import chardet
from BeautifulSoup import BeautifulSoup

class EmailObject:
  CLRF = "\n\r\n\r"
  def __init__(self, file, category = None):
    self.file = file
    self.category = category
    self.mail = email.message_from_file(self.file)
    self.file.close()

  def subject(self):
    return self.mail.get('Subject')

  def body(self):
    payload = self.mail.get_payload()
    parts = []
    if self.mail.is_multipart():
      parts = [self.single_body(part) for part in list(payload)]
    else:
      parts = [self.single_body(self.mail)]
    return self.CLRF.join(parts)
      
  def single_body(self, part):
    content_type = part.get_content_type()
    body = part.get_payload(decode=True)

    if content_type == 'text/html':
      return BeautifulSoup(body).text 
    elif content_type == 'text/plain':
      return body
    else:
      return ''
