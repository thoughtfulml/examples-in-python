# coding=utf-8
import codecs
import os
import re
from future.standard_library import install_aliases

install_aliases()

from urllib.parse import urlencode

import requests
from bs4 import BeautifulSoup

root_url = "http://www.biblegateway.com/passage/"

languages = {
  'English': {
    'version': 'ESV',
    'search': ['Matthew', 'Acts']
  },
  'Dutch': {
    'version': 'HTB',
    'search': ['Mattheüs', 'Handelingen']
  },
  'Polish': {
    'version': 'SZ-PL',
    'search': ['Ewangelia według św. Mateusza', 'Dzieje Apostolskie']
  },
  'German': {
    'version': 'HOF',
    'search': ['Matthaeus', 'Apostelgeschichte']
  },
  'Finnish': {
    'version': 'R1933',
    'search': ['Matteuksen', 'Teot']
  },
  'Swedish': {
    'version': 'SVL',
    'search': ['Matteus', 'Apostlagärningarna']
  },
  'Norwegian': {
    'version': 'DNB1930',
    'search': ['Matteus', 'Apostlenes-gjerninge']
  }
}

cleaning_re = re.compile(r'[\d,;:\\\-\"]', )

for language, search_pattern in languages.items():
  text = ''
  for i, search in enumerate(search_pattern['search']):
    for page in range(1, 29):
      print("Querying %s %s chapter %d" % (language, search, page))
      query_string = urlencode({
        'search': '%s %d' % (search, page),
        'version': search_pattern['version']
      })
      url = root_url + '?' + query_string
      print(url)

      r = requests.get(url)
      soup = BeautifulSoup(r.text, 'html.parser')
      for verse in soup.select('.text-html p'):
        cleaned_verse = cleaning_re.sub('', verse.text).strip()
        text += ' ' + cleaned_verse.lower()
    file_path = os.path.join('..', 'data', '%s_%d.txt' % (language, i))
    with(codecs.open(file_path,
                     mode='w',
                     encoding='utf-8')) as f:
      f.write(text)
