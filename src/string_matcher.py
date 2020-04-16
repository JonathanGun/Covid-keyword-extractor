from typing import List
from typing_extensions import Final
import itertools
import re


class StringMatcher:
    def __init__(self, strategy):
        self.strategy = strategy

    def change_strategy(self, strategy):
        self.strategy = strategy

    def match(self, txt, pat):
        return self.strategy.match(txt, pat)


class MatchStrategy:
    def match(self, txt: str, pat: str) -> int:
        pass


class BoyerMoore(MatchStrategy):
    ASCII: Final[int] = 128

    def __buildLast(self, string) -> List[int]:
        last: List[int] = [-1] * BoyerMoore.ASCII
        for i in range(len(string)):
            last[ord(string[i])] = i
        return last

    def match(self, txt, pat):
        last = self.__buildLast(pat)
        n, m = len(txt), len(pat)
        if(m > n):
            return -1  # no match if pat > txt

        i = j = m - 1
        while True:
            if pat[j] == txt[i]:
                if j == 0:
                    return i
                else:  # looking glass
                    i -= 1
                    j -= 1
            else:  # charater jump
                lo: int = last[ord(txt[i])]  # last occ
                i += m - min(j, lo + 1)
                j = m - 1

            if(i > n - 1):
                break
        return -1  # no match


class KMP(MatchStrategy):
    def __compute_fail(self, string) -> List[int]:
        m = len(string)
        fail = [0] * m
        i, j = 1, 0

        while i < m:
            if (string[j] == string[i]):  # j+ 1 chars match
                fail[i] = j + 1
                j += 1
                i += 1
            elif j > 0:  # j follows matching prefix
                j = fail[j - 1]
            else:  # no match
                fail[i] = 0
                i += 1
        return fail

    def match(self, txt, pat):
        n, m = len(txt), len(pat)
        fail = self.__compute_fail(pat)
        i = j = 0
        while i < n:
            if pat[j] == txt[i]:
                if j == m - 1:
                    return i - m + 1
                i += 1
                j += 1
            elif j > 0:
                j = fail[j - 1]
            else:
                i += 1
        return -1  # no match


class Regex(MatchStrategy):
    def match(self, txt, pat):
        matches = list(itertools.islice(re.finditer(pat, txt), 1))
        return matches[0].span()[0] if len(matches) else -1
