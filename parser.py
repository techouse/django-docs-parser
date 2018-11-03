#!/usr/bin/env python
import json
import os.path
import re
from io import BytesIO
from urllib.parse import urljoin
from zipfile import ZipFile

import requests
from bs4 import BeautifulSoup

DJANGO_VERSIONS = ('2.1', '1.11')
DJANGO_DOCS_DOWNLOAD_URL = 'https://docs.djangoproject.com/m/docs/django-docs-{version}-en.zip'
DJANGO_DOCS_URL = 'https://docs.djangoproject.com/en/{version}/'

EXCLUDED_IDS = {'term-', 'allow_migrate-', 'allow_relation-', 'index-'}


def parse():
    entries = []

    for version in DJANGO_VERSIONS:
        with ZipFile(BytesIO(requests.get(DJANGO_DOCS_DOWNLOAD_URL.format(version=version)).content)) as zipfile:
            with zipfile.open('genindex.html') as genindex:
                index_soup = BeautifulSoup(genindex, 'lxml')

                for index, table in enumerate(index_soup.find_all('table', class_='genindextable')):
                    if index < 2:
                        # skip first 2 tables listing Symbols and dunder methods
                        continue

                    for a in table.find_all('a'):
                        href = a.get('href')
                        file, id = href.split('#')

                        if file.startswith('releases/') or any(id.startswith(pattern) for pattern in EXCLUDED_IDS):
                            continue

                        with zipfile.open(file) as html:
                            try:
                                topic_soup = BeautifulSoup(html, 'lxml')
                                topic = topic_soup.find(id=id)
                                parent = topic.parent

                                entry_data = {
                                    'version': float(version),
                                    'id': id.replace('std:', '') if id.startswith('std:') else id,
                                    'title': '',
                                    'permalink': urljoin(DJANGO_DOCS_URL.format(version=version),
                                                         href.replace('.html', '/')),
                                    'categories': [],
                                    'content': ''
                                }

                                if parent.name == 'dl' and topic.name == 'dt':
                                    # set the title
                                    if any(character.isupper() for character in id):
                                        entry_data['title'] = id[re.search('[A-Z]', id).start():]
                                    else:
                                        if topic.find(class_='descclassname'):
                                            entry_data['title'] += topic.find(class_='descclassname').get_text()
                                        if topic.find(class_='descname'):
                                            entry_data['title'] += topic.find(class_='descname').get_text()
                                        if parent.get('class') == 'glossary docutils':
                                            entry_data['title'] += topic.get_text()
                                    # set the content
                                    if parent.find('dd').find('p'):
                                        entry_data['content'] = ' '.join(parent.find('dd').find('p').get_text().split())
                                    # set the categories
                                    if topic.find(class_='property'):
                                        entry_data['categories'].append(topic.find(class_='property').get_text())
                                    if id.startswith('django.'):
                                        entry_data['categories'] += id.split('.')[1:-1]
                                else:
                                    if id.startswith('std:'):
                                        if ':setting-' in id:
                                            # set the title
                                            entry_data['title'] = id.split('-')[-1]
                                            # set the categories
                                            entry_data['categories'].append(re.split(r'[:\-]', id)[1])
                                            # set te content
                                            if len(parent.find_all('p')) > 1:
                                                entry_data['content'] = ' '.join(
                                                    parent.find_all('p')[1].get_text().split())
                                            else:
                                                entry_data['content'] = ' '.join(parent.find('p').get_text().split())
                                        elif ':templatefilter-' in id:
                                            # set the title
                                            entry_data['title'] = id.split('-')[-1]
                                            # set the categories
                                            entry_data['categories'].append(re.split(r'[:\-]', id)[1])
                                            # set te content
                                            entry_data['content'] = ' '.join(parent.find('p').get_text().split())
                                        elif ':fieldlookup-' in id:
                                            # set the title
                                            entry_data['title'] = id.split('.')[-1]
                                            # set the categories
                                            entry_data['categories'].append(re.split(r'[:\-.]', id)[1])
                                            # set te content
                                            if parent.find('p'):
                                                entry_data['content'] = ' '.join(parent.find('p').get_text().split())
                                        elif ':templatetag-' in id:
                                            # set the title
                                            entry_data['title'] = id.split('-')[-1]
                                            # set the categories
                                            entry_data['categories'].append(re.split(r'[:\-]', id)[1])
                                            # set te content
                                            entry_data['content'] = ' '.join(parent.find('p').get_text().split())

                                entries.append(entry_data)
                            except:
                                print(href)
                                print(parent.name)
                                raise

    if entries:
        with open(os.path.abspath('data.json'), 'w') as fh:
            json.dump(entries, fh, indent=4)


if __name__ == '__main__':
    parse()
