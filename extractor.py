from typing import List
from string_matcher import StringMatcher
import re
import string
import nltk

DEBUG = True


def sent_tokenize(text: str) -> List[str]:
    sent_detector = nltk.data.load('libs/english_tokenizer.pickle')
    return sent_detector.tokenize(text.strip())


class Match:
    def __init__(self, keyword, sentence, date, num):
        self.keyword = keyword
        self.sentence = sentence
        self.date = date
        self.num = num
        self.sentence = self.sentence.replace(self.keyword, "<b>" + self.keyword + "</b>")
        self.sentence = self.sentence.replace(self.date, "<b>" + self.date + "</b>")
        for n in self.num:
            self.sentence = self.sentence.replace(n, "<b>" + n + "</b>")
        self.num = " | ".join(self.num)
        self.weak = num == []


class Extractor:
    def __init__(self, keywords: List[str], matcher: StringMatcher = StringMatcher()):
        self.keywords = keywords
        self.matcher = matcher

    def __remove_non_printable_char(self, text: str) -> str:
        return ''.join(filter(lambda x: x in set(string.printable), text))

    def __add_period_to_eol(self, text: str) -> str:
        return re.sub(r'(?<=[^.\n])(?:\n+)(?=[^\n])', r'. ', text, re.M)

    def __preprocess_text(self, text: str) -> str:
        text = self.__remove_non_printable_char(text).strip()
        print("======================before")
        print(repr(text))
        text = self.__add_period_to_eol(text)
        print("======================after")
        print(repr(text))
        return text

    def __list_to_regex_union(self, patterns: List[str]) -> str:
        return "(?:" + "|".join(patterns) + ")"

    def __find_util(self, patterns, text: str):
        return (text[match.start():match.end()] for match in re.finditer(self.__list_to_regex_union(patterns), text.lower()))

    def __find_dates(self, text: str):
        months = [
            "januari", "februari", "maret", "april", "juni", "juli", "agustus", "september", "november", "desember",
            "january", "february", "march", "june", "july", "august", "december"
            "jan", "feb", "mar", "apr", "mei", "jun", "jul", "ags", "sep", "sept", "nov", "des",
            "may", "aug", "dec"
        ]
        patterns = [
            r"(?:(?<=\D)|^)\d{1,2}\/\d{1,2}\/\d{4}(?:(?=\D)|$)",
            r"(?:(?<=\D)|^)\d{1,2} " + self.__list_to_regex_union(months) + r" \d{4}(?:(?=\D)|$)",
            r"(?:(?<=\D)|^)\d{1,2} " + self.__list_to_regex_union(months) + r"(?:(?=\D)|$)",
            self.__list_to_regex_union(months) + r" (?:(?<=\D)|^)\d{1,2}," + r" \d{4}(?:(?=\D)|$)",
            self.__list_to_regex_union(months) + r" (?:(?<=\D)|^)\d{1,2}",
        ]
        return self.__find_util(patterns, text)

    def __find_times(self, text: str):
        timezones = [
            "wib", "wita", "wit",
            r"gmt\+\d{1,2}",
            r"(?:[a|p]\.m\.) gmt\+\d{1,2}",
            "am", "pm",
        ]
        patterns = [
            r"(?:(?<=\D)|^)\d{1,2}[:|.]\d{2}(?: " + self.__list_to_regex_union(timezones) + r"|(?=\D)|$)",
        ]
        return self.__find_util(patterns, text)

    def __find_days(self, text: str):
        patterns = [
            "senin", "selasa", "rabu", "kamis", "jumat", "sabtu", "minggu",
            "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday",
            r"(?:se|\w )hari(?: sebelumnya| setelahnya|[^0-9a-zA-Z])",
        ]
        return self.__find_util(patterns, text)

    def __find_nums(self, text: str) -> List[str]:
        numbers = {
            "id": [
                "satu", "dua", "tiga", "empat", "lima", "enam", "tujuh", "delapan", "sembilan", "sepuluh",
                "sebelas", r"\w+ belas", r"\w+ puluh", r"\w+ ratus", r"\w+ ribu", r"\w+ juta"
            ],
            "en": [
                "a", "an" "one",
                "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten",
                "eleven", "twelve", r"\S+teen",
            ],
        }
        patterns = [
            "seorang", "sebuah kasus", "beberapa",
            r"(?:(?:(?<=\s)|^)(?:(?:\d{1,3}(?:\.\d{3})*(?:\.\d+)|\d+))| " + self.__list_to_regex_union(numbers["id"]) + ")" + " (?:pasien|orang|kasus)",
            r"(?:(?:(?<=\s)|^)(?:(?:\d{1,3}(?:,\d{3})*(?:,\d+)|\d+))|" + self.__list_to_regex_union(numbers["en"]) + ")" + r" (?:patient|people|case|\w case|\w \w case|confirmed|death)",
            r"(?:(?<=\s)|^)(?:\d+(?:,\d{3})*(?:,\d+))",
            self.__list_to_regex_union(["as", "additional", "of", "to"]) + r" (?:(?<=\s)|^)(?:\d+)(?=[^,])",
            "some", "many", "most"
        ]
        return self.__find_util(patterns, text)

    def __find_date_time(self, text: str) -> str:
        day = next(self.__find_days(text), "")
        date = next(self.__find_dates(text), "")
        time = next(self.__find_times(text), "")
        day += ", " if (day and date) else ""
        date += " " if time else ""
        return day + date + time

    def extract(self, text: str, allow_weak: bool = True):
        matches = []
        text = self.__preprocess_text(text)
        first_sentence = True
        meta = {}
        weak_cnt = 0
        for sentence in sent_tokenize(text):
            print(sentence)
            for keyword in self.keywords:
                idx = self.matcher.match(sentence.strip(), keyword.strip())
                if idx != -1 or first_sentence:
                    date = self.__find_date_time(sentence)
                    num = list(set(self.__find_nums(sentence)))
                    if first_sentence:
                        meta["date"] = date
                        keyword = "<i>headline</i>"
                        first_sentence = False
                    date = date if date else meta["date"] + " - tanggal terbit artikel"

                    if (date and num) or allow_weak:
                        weak_cnt += 1 if not (date and num) else 0
                        matches.append(Match(keyword, sentence, date, num))
                        print("===MATCH===" if date and num else "===WEAK MATCH===")
                        print("Keyword:", keyword)
                        print("Jumlah:", num, ";Waktu:", date)
                        print(sentence)
                        print()
                        break
        print(f"Found {len(matches)} match(es), {weak_cnt} are weak match(es)")
        return matches
