from enum import Enum, auto
from typing import List
from lxml import etree

from n3xt_crawler_py.web_crawler.crawl_xpath import CrawlXpath


class CrawlParseMode(Enum):
    """문서 파싱 모드 (HTML 또는 XML)."""

    HTML = auto()
    XML = auto()


class CrawlParser:
    """HTML 또는 XML 문서를 파싱하고 XPath로 데이터를 추출하는 클래스."""

    def __init__(self, content: str, mode: CrawlParseMode):
        """CrawlParser 초기화.

        Args:
            content (str): 파싱할 원시 문서 (HTML/XML 문자열).
            mode (CrawlParseMode): 문서 파싱 모드 (HTML 또는 XML).

        Raises:
            ValueError: 지원하지 않는 파싱 모드인 경우.
        """
        self.__mode: CrawlParseMode = mode

        if mode not in (CrawlParseMode.XML, CrawlParseMode.HTML):
            cls = self.__class__.__name__
            raise ValueError(f"[{cls}] Unsupported parse mode: '{mode.name}'")

        self.__root = self.__parse_root(content)

    def __parse_root(self, content: str):
        """내부 문서 파서.

        Args:
            content (str): HTML 또는 XML 콘텐츠 문자열.

        Returns:
            etree._Element: 루트 엘리먼트.

        Raises:
            ValueError: 콘텐츠가 잘못된 형식일 경우.
        """
        try:
            if self.__mode == CrawlParseMode.XML:
                return etree.fromstring(content)
            elif self.__mode == CrawlParseMode.HTML:
                return etree.HTML(content)
            else:
                cls = self.__class__.__name__
                raise RuntimeError(f"[{cls}] Unreachable parse mode: '{self.__mode}'")
        except etree.XMLSyntaxError as e:
            cls = self.__class__.__name__
            raise ValueError(f"[{cls}] Invalid {self.__mode.name} content: {e}") from e

    def get_blocks(self, xpath: CrawlXpath) -> List[etree._Element]:
        """지정된 XPath에 해당하는 블록 요소들을 반환합니다.

        Args:
            xpath (CrawlXpath): 반복 블록을 찾기 위한 XPath.

        Returns:
            List[etree._Element]: 일치하는 엘리먼트 목록.

        Raises:
            ValueError: 유효하지 않은 XPath 표현식일 경우.
        """
        try:
            return self.__root.xpath(xpath.str)
        except etree.XPathEvalError as e:
            cls = self.__class__.__name__
            raise ValueError(f"[{cls}] Invalid block XPath: '{xpath.str}' - {e}") from e

    def extract_field(
        self, block: etree._Element, field_xpath: CrawlXpath
    ) -> List[str]:
        """지정된 XPath를 사용해 블록 내에서 필드 값을 추출합니다.

        Args:
            block (etree._Element): 추출 대상 블록 요소.
            field_xpath (CrawlXpath): 필드에 해당하는 XPath.

        Returns:
            List[str]: 추출된 텍스트 또는 속성 목록.

        Raises:
            ValueError: XPath 표현식이 잘못된 경우.
        """
        try:
            return block.xpath(field_xpath.str)
        except etree.XPathEvalError as e:
            cls = self.__class__.__name__
            raise ValueError(
                f"[{cls}] Invalid field XPath: '{field_xpath.str}' - {e}"
            ) from e
