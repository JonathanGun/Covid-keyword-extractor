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

    test_long: Final[Dict[str, List[Tuple[str, int]]]] = {
        "Konfirmasi positif coronavirus atau Covid-19 dari pemeriksaan PCR menjadi 5.516 orang,": [
            ("positif", 11),
            ("PCA", -1),
            ("Kon", 0)
        ]
    }

    def __util(self, Strategy, test_case: Dict[str, List[Tuple[str, int]]]) -> int:
        matcher = StringMatcher(Strategy())
        for txt, pats in test_case.items():
            for pat in pats:
                match = matcher.match(txt, pat[0])
                assert match == pat[1]
                return match
        return -1

    def test_boyer_moore(self) -> None:
        self.__util(BoyerMoore, self.test_simple)
        self.__util(BoyerMoore, self.test_long)

    def test_kmp(self) -> None:
        self.__util(KMP, self.test_simple)
        self.__util(KMP, self.test_long)

    def test_regex(self) -> None:
        self.__util(Regex, self.test_simple)
        self.__util(Regex, self.test_long)

    def test_integrate(self) -> None:
        assert self.__util(KMP, self.test_simple) == self.__util(Regex, self.test_simple)
        assert self.__util(KMP, self.test_simple) == self.__util(BoyerMoore, self.test_simple)
        assert self.__util(KMP, self.test_long) == self.__util(Regex, self.test_long)
        assert self.__util(KMP, self.test_long) == self.__util(BoyerMoore, self.test_long)
