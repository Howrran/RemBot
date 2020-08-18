"""
Manager for working with Google Document
"""
from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.errors import HttpError

class DocManager():
    """
     The file token.pickle stores the user's access and refresh tokens, and is created automatically
     when the authorization flow completes for the first     time.
    """
    # If modifying these scopes, delete the file token.pickle.
    SCOPES = ['https://www.googleapis.com/auth/documents.readonly']

    DOCUMENT_ID = '1j-v9OfrngzZ9-or7guRVIV5bjLQ7A0ninbIwOkZKg4k'

    @staticmethod
    def read_paragraph_element(element):
        """Returns the text in the given ParagraphElement.

            Args:
                element: a ParagraphElement from a Google Doc.
        """
        text_run = element.get('textRun')
        if not text_run:
            return ''
        return text_run.get('content')

    @staticmethod
    def read_strucutural_elements(elements):
        """
        Recurses through a list of Structural Elements to read a document's text where text may be
        in nested elements.

            Args:
                elements: a list of Structural Elements.
        """
        text = ''
        for value in elements:
            if 'paragraph' in value:
                elements = value.get('paragraph').get('elements')
                for elem in elements:
                    text += DocManager.read_paragraph_element(elem)
            elif 'table' in value:
                # The text in table cells are in nested Structural Elements and tables may be
                # nested.
                table = value.get('table')
                for row in table.get('tableRows'):
                    cells = row.get('tableCells')
                    for cell in cells:
                        text += DocManager.read_strucutural_elements(cell.get('content'))
            elif 'tableOfContents' in value:
                # The text in the TOC is also in a Structural Element.
                toc = value.get('tableOfContents')
                text += DocManager.read_strucutural_elements(toc.get('content'))
        return text

    @staticmethod
    def get_doc_content(document_id=None):
        """
        Read content of the Google Document
        :return: str: document content
        """
        creds = None

        # import os
        # cwd = os.getcwd()
        # print(cwd)

        document_id = document_id if document_id else DocManager.DOCUMENT_ID
        if os.path.exists('../token.pickle'):
            with open('../token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', DocManager.SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('../token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        service = build('docs', 'v1', credentials=creds)

        # Retrieve the documents contents from the Docs service.
        try:
            document = service.documents().get( #pylint: disable= no-member
                documentId=document_id) \
                .execute()
        except HttpError:
            print('google doc error')
            return None

        doc_content = document.get('body').get('content')
        text = DocManager.read_strucutural_elements(doc_content)

        return text

    @staticmethod
    def parse_line(line):
        """
        parse line and return dict word - translation(or None if absent)

        :param line: str
        :return: dict
        """
        data = {}
        line = line.split('-')

        if len(line) > 1:
            translation = line[-1].strip()
            word = ''.join(line[:-1]).strip()
            data[word] = translation

        else:
            if word := line[0]:
                data[word] = None

        return data


    @staticmethod
    def get_words_in_dictionary(document_id=None):
        """
        Get content from google document and return a dict{word : translation}

        :param document_id: str
        :return: dict
        """
        document_id = document_id if document_id else DocManager.DOCUMENT_ID

        content = DocManager.get_doc_content(document_id)
        if content is None:
            return None
        dictionary = {}

        for line in content.split('\n'):
            dictionary.update(DocManager.parse_line(line)) # update dict {word : translation}

        return dictionary
