import os

import pymorphy2

from io import StringIO
from typing import List

from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser


class DocumentHandler:
    _analyzer = pymorphy2.MorphAnalyzer()
    _ignored_lexems = ["можно", "всей"]
    _punctuation_marks = [",", "!", "?", "`", "\"", "\\", "|", "/", "\n", "%", "-"]
    _incorrect_pos = ["NPRO", "PREP", "NUMR", "CONJ", "PRCL", "INTJ", "PRED", "COMP", "ADVB"]

    def __init__(self, doc_path: str):
        self._file_name = doc_path

    @staticmethod
    def convert_pdf_to_string(file_path: str) -> str:
        output_string = StringIO()
        with open(file_path, 'rb') as in_file:
            parser = PDFParser(in_file)
            doc = PDFDocument(parser)
            manager = PDFResourceManager()
            device = TextConverter(manager, output_string, laparams=LAParams())
            interpreter = PDFPageInterpreter(manager, device)
            for page in PDFPage.create_pages(doc):
                interpreter.process_page(page)

        return output_string.getvalue()[:-3]

    def get_file_path(self) -> str:
        return os.path.abspath(self._file_name)

    def _is_correct_pos(self, lexeme: str) -> bool:
        result = self._analyzer.parse(lexeme)
        for pos in self._incorrect_pos:
            if pos in result[0].tag:
                return False
        return True

    def _replace_punctuation(self, word: str) -> str:
        for mark in self._punctuation_marks:
            word = word.replace(mark, "")
        return word

    def get_lexems(self) -> List[str]:
        text = self.convert_pdf_to_string(self.get_file_path())
        sentences = text.split(".")
        words = []
        for sentence in sentences:
            word = sentence.split()
            for wrd in word:
                if (wrd not in self._ignored_lexems) and (self._is_correct_pos(wrd)) and (wrd.isalpha()):
                    wrd = self._replace_punctuation(wrd)
                    words.append(wrd.lower())
        words = list(set(words))
        words.sort(key=str.lower)
        return words
