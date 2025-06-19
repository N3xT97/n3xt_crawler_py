from lxml import etree
from dataclasses import dataclass


@dataclass(frozen=True)
class CrawlXpath:
    """XPath 문자열을 감싸는 불변 데이터 클래스.

    생성 시 유효한 XPath인지 검증합.

    Attributes:
        str (str): XPath 표현 문자열.
    """

    str: str

    def __post_init__(self):
        """객체 생성 후 XPath 유효성 검사 수행."""
        self.__validate_xpath(self.str)

    def __validate_xpath(self, xpath: str) -> None:
        """XPath 문자열의 문법을 검증.

        Args:
            xpath (str): 검사할 XPath 문자열.

        Raises:
            ValueError: XPath 구문 오류가 있는 경우.
        """
        try:
            etree.XPath(xpath)
        except etree.XPathSyntaxError as e:
            raise ValueError(
                f"[{self.__class__.__name__}] Invalid XPath: '{xpath}' - {e}"
            ) from e
