import email
from BeautifulSoup import BeautifulSoup

class EmailObject:
  def __init__(self, filepath, category = None):
    self.filepath = filepath
    self.category = category
    self.mail = email.message_from_file(self.filepath)

  def subject(self):
    return self.mail.get('Subject')

  def body(self):
    if self.mail.is_multipart():
      return self.multipart_body()
    else:
      return self.single_body()

  def single_body(self, part = None):
    if not part:
      part = self.mail
    content_type = part.get_content_type()
    body = part.get_payload(decode=True)

    if content_type == 'text/html':
      return BeautifulSoup(body).text 
    elif content_type == 'text/plain':
      return body 
    else:
      return ''

  def multipart_body(self):
    output = ''
    for part in self.mail.walk():
      output += self.single_body(part=part)
    return output



