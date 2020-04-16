from string_matcher import StringMatcher, BoyerMoore, KMP, Regex
from typing import Dict, Tuple, List
from typing_extensions import Final


class TestClass:
    test_simple: Final[Dict[str, List[Tuple[str, int]]]] = {
        "AA": [
            ("A", 0),
            ("B", -1),
        ],
        "ABCA": [
            ("A", 0),
            ("B", 1),
            ("C", 2),
            ("BC", 1),
            ("CA", 2),
        ],
    }

    def __util(self, Strategy, test_case: Dict[str, List[Tuple[str, int]]]) -> None:
        matcher = StringMatcher(Strategy())
        for txt, pats in test_case.items():
            for pat in pats:
                assert matcher.match(txt, pat[0]) == pat[1]

    def test_boyer_moore(self) -> None:
        self.__util(BoyerMoore, self.test_simple)

    def test_kmp(self) -> None:
        self.__util(KMP, self.test_simple)

    def test_regex(self) -> None:
        self.__util(Regex, self.test_simple)
