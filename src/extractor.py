from typing import List
from string_matcher import StringMatcher
import re


class Match:
    def __init__(self, keyword, sentence):
        self.keyword = keyword
        self.sentence = sentence

    def __repr__(self):
        return self.keyword + "\n" + self.sentence


class Extractor:
    def __init__(self, keywords: List[str], matcher: StringMatcher = StringMatcher()):
        self.keywords = keywords
        self.matcher = matcher

    def __parse_text_to_sentences(self, text: str) -> List[str]:
        # sentences = []
        # for element in self.text:
        #     sentences += re.split("(?<=[.!?])\s+", element)
        # return sentences
        return text.split(".")

    def extract(self, text: str):
        matches = []
        for sentence in self.__parse_text_to_sentences(text):
            for keyword in self.keywords:
                idx = self.matcher.match(sentence, keyword)
                if idx != -1:
                    matches.append(Match(keyword, sentence))
                    break
        return matches

    def __repr__(self):
        string = ""
        string += "filename: " + self.filename + "\n"
        string += "kwd: " + ",".join(self.keywords) + "\n"
        string += "matches:\n" + "\n".join([repr(match) for match in self.matches])
        return string
