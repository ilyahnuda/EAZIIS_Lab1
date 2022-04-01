from typing import Dict

import pymorphy2

cases_representation = {"nomn": "Именительный", "gent": "Родительный", "datv": "Дательный",
                        "accs": "Винительный", "ablt": "Творительный", "loct": "Предложный"}
pos_representation = {"СУЩ": "Существительное", "ГЛ": "Глагол", "ПРИЛ": "Прилагательное",
                      "КР_ПРИЧ": "Краткое причастие", "СОЮЗ": "Союз", "ПР": "Предлог",
                      "КР_ПРИЛ": "Краткое прилагательное", "КОМП": "Компаротив", "ИНФ": "Инфинитив",
                      "ПРИЧ": "Причастие", "ДЕЕПР": "Деепричастие", "ЧИСЛ": "Числительное", "Н": "Наречие",
                      "МС": "Местоимение", "ЧАСТ": "Частица", "МЕЖД": "Междометие"}


class LexemeHandler:
    def __init__(self, lexeme: str):
        self._lexeme = lexeme
        self._analyzer = pymorphy2.MorphAnalyzer()
        self._parsed = self._analyzer.parse(lexeme)[0]
        self._plural_cases = []  # склонения во множественном числе
        self._cases = []  # склонения
        self._current_case = ""
        self._generate_cases()
        self._part_of_speech = self._analyzer.lat2cyr(self._parsed.tag.POS)  # часть речи
        self._normal_form = self._parsed.normal_form  # начальная форма
        self._stem = self._get_stem()  # основа слова
        self._struct = {}
        self._generate_lexeme_struct()

    def _generate_cases(self):
        try:
            for case in cases_representation.keys():
                case_word = self._parsed.inflect({case}).word
                self._cases.append(case_word)
                if self._current_case == "" and case_word == self._lexeme:
                    self._current_case = cases_representation.get(case)

            for case in cases_representation.keys():
                case_word = self._parsed.inflect({'plur', case}).word
                self._plural_cases.append(case_word)
                if self._current_case == "" and case_word == self._lexeme:
                    self._current_case = cases_representation.get(case)
        except AttributeError:
            print("Не найдено разбора для лексемы \"" + self._lexeme + "\"")

    def _get_stem(self):
        if len(self._cases) == 1:
            return self._cases[0]
        if not self._cases or len(self._cases[0]) == 0:
            return ""
        stem = ""
        for i in range(len(self._cases[0])):
            for j in range(len(self._cases[0]) - i + 1):
                if j > len(stem) and all(self._cases[0][i:i + j] in x for x in self._cases):
                    stem = self._cases[0][i:i + j]
        return stem

    def _generate_lexeme_struct(self):
        if self._current_case == "":
            self._current_case = "Отсутствует"
        if self._stem == "":
            self._stem = "Не определена"
        self._struct = {self._lexeme: {"Часть речи": pos_representation.get(self._part_of_speech),
                                       "Начальная форма": self._normal_form,
                                       "Основа": self._stem,
                                       "Падеж": self._current_case}}

    def generate_wordform(self, case_ru: str, singular: bool):
        if case_ru not in cases_representation.values():
            return ""
        self._current_case = case_ru
        case = self._get_key_case(case_ru)
        if singular:
            self._lexeme = self._parsed.inflect({case}).word
        self._lexeme = self._parsed.inflect({'plur', case}).word
        self._generate_lexeme_struct()
        return self.get_lexeme_struct()

    @staticmethod
    def _get_key_case(value):
        for case_key, case_ru in cases_representation.items():
            if case_ru == value:
                return case_key

    def get_lexeme_struct(self) -> Dict:
        return self._struct

    def print_lexeme_struct(self):
        for key, value in self._struct.items():
            print(f"{key}: {value}")
