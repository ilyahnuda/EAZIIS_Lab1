from typing import List, Dict

from ..document_handler.document_handler import DocumentHandler
from ..lexeme_handler.lexeme_handler import LexemeHandler


class DictionaryHandler:
    def __init__(self, document_path: str):
        self._document_handler = DocumentHandler(document_path)
        self._dictionary = []
        self._create_dictionary()

    def _get_lexems(self) -> List[str]:
        return self._document_handler.get_lexems()

    def _create_dictionary(self):
        for lexeme in self._get_lexems():
            self._dictionary.append(LexemeHandler(lexeme).get_lexeme_struct())

    def get_lexeme_structure(self, lexeme: str) -> Dict:
        for structure in self._dictionary:
            lex, struct = list(structure.items())[0]
            if lex == lexeme:
                return struct
        return {}

    def edit_lexeme_structure(self, lexeme: str, prop: str, value):
        structure = self.get_lexeme_structure(lexeme)
        structure[prop] = value

    def add_lexeme_structure(self, lexeme: str):
        self._dictionary.append(LexemeHandler(lexeme).get_lexeme_struct())

    def generate_wordform(self, lexeme: str, case_ru: str, singular: bool):
        self._dictionary.append(LexemeHandler(lexeme).generate_wordform(case_ru, singular))

    def append_document(self, document_path):
        document_handler = DocumentHandler(document_path)
        for lexeme in document_handler.get_lexems():
            if lexeme not in self._get_lexems():
                self._dictionary.append(LexemeHandler(lexeme).get_lexeme_struct())

    def get_lexeme_structures_by_pos(self, part_of_speech: str) -> str:
        structures = ""
        number = 1
        for struct in self._dictionary:
            if list(struct.values())[0].get("Часть речи") == part_of_speech:
                structures += str(number) + ". " + self.get_dictionary_string(struct) + "\n"
                number += 1
        return structures

    def get_lexeme_structures_by_case(self, case: str) -> str:
        structures = ""
        number = 1
        for struct in self._dictionary:
            if list(struct.values())[0].get("Падеж") == case:
                structures += str(number) + ". " + self.get_dictionary_string(struct) + "\n"
                number += 1
        return structures

    def get_lexeme_structure_by_normal_form(self, normal_form: str) -> str:
        structure = ""
        for struct in self._dictionary:
            if list(struct.values())[0].get("Начальная форма") == normal_form:
                structure += remove_structure_symbols(str(self.get_lexeme_structure(list(struct.keys())[0])))
                break
        return structure

    def get_dictionary_string(self, dictionary):
        string = ""
        for struct in dictionary:
            string += remove_structure_symbols(str(struct))
        return string

    @staticmethod
    def get_full_dictionary_string(dictionary):
        string = ""
        number = 1
        for struct in dictionary:
            string += " " + str(number) + ". " + remove_structure_symbols(str(struct)) + "\n"
            number += 1
        return string

    def get_dictionary(self) -> List:
        return self._dictionary


def remove_structure_symbols(structure: str):
    for symbol in ["{", "}", "]", "[", "'"]:
        structure = structure.replace(symbol, "")
    return structure
