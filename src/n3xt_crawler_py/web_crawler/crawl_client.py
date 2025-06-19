from typing import Dict, List

from n3xt_crawler_py.data_parser.crawl_parser import CrawlParseMode, CrawlParser
from n3xt_crawler_py.web_crawler.crawl_requester import CrawlRequestMode, CrawlRequester
from n3xt_crawler_py.web_crawler.crawl_url import CrawlUrl
from n3xt_crawler_py.web_crawler.crawl_xpath import CrawlXpath


class CrawlClient:
    """웹 페이지에서 데이터를 추출하기 위한 고수준 크롤링 클라이언트."""

    def __init__(
        self,
        url: str,
        req_mode: CrawlRequestMode,
        parse_mode: CrawlParseMode,
    ):
        """CrawlClient 생성자.

        Args:
            url (str): 요청할 웹 페이지의 URL.
            req_mode (CrawlRequestMode): 요청 방식 (예: DEFAULT, DYNAMIC 등).
            parse_mode (CrawlParseMode): 파싱 모드 (HTML 또는 XML).

        Raises:
            ValueError: 응답이 비어 있거나 파싱에 실패한 경우 내부적으로 발생할 수 있음.
        """
        try:
            self.__response = CrawlRequester(CrawlUrl(url), req_mode).get_response()
            self.__parser = CrawlParser(self.__response.get_content(), parse_mode)
        except Exception as e:
            cls = self.__class__.__name__
            raise RuntimeError(f"[{cls}] Failed to initialize: {e}") from e

    def extract_fields(
        self,
        block_xpath: str,
        fields_map: Dict[str, str],
    ) -> List[Dict[str, List[str]]]:
        """지정된 XPath를 기준으로 데이터 블록을 추출하고, 각 필드를 매핑하여 추출합니다.

        Args:
            block_xpath (str): 반복되는 데이터 블록을 선택할 XPath.
            fields_map (Dict[str, str]): {필드이름: 필드 XPath} 구조의 딕셔너리.

        Returns:
            List[Dict[str, List[str]]]: 추출된 블록별 필드 데이터 목록.
                예: [{"title": ["A"], "url": ["http://..."]}, ...]

        Raises:
            ValueError: 잘못된 XPath 또는 파싱 오류 발생 시 내부적으로 발생.
        """
        try:
            blocks = self.__parser.get_blocks(CrawlXpath(block_xpath))
        except Exception as e:
            cls = self.__class__.__name__
            raise ValueError(f"[{cls}] Invalid block XPath '{block_xpath}': {e}") from e

        results: List[Dict[str, List[str]]] = []

        for block in blocks:
            extracted: Dict[str, List[str]] = {}
            for tag, field_xpath in fields_map.items():
                try:
                    extracted[tag] = self.__parser.extract_field(
                        block, CrawlXpath(field_xpath)
                    )
                except Exception as e:
                    cls = self.__class__.__name__
                    raise ValueError(
                        f"[{cls}] Failed to extract field '{tag}' with XPath '{field_xpath}': {e}"
                    ) from e
            results.append(extracted)

        return results
