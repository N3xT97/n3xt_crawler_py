import requests


class CrawlResponse:
    """requests.Response 객체를 감싸서 응답 내용을 디코딩하고 상태 정보를 제공하는 클래스.

    Attributes:
        __BASIC_ENCODING (str): 기본 문자 인코딩 (utf-8).
        __INVALID_RESPONSE_FILTER (list[str]): 응답 내용 내 비정상 메시지 필터 리스트.
        __content (str): 디코딩된 응답 본문.
        __status (int): HTTP 상태 코드.
        __content_type (str): 응답 Content-Type 헤더 (소문자 변환).
    """

    __BASIC_ENCODING = "utf-8"
    __INVALID_RESPONSE_FILTER = ["502 Bad Gateway"]

    def __init__(self, resp: requests.Response):
        """CrawlResponse 생성자.

        Args:
            resp (requests.Response): requests 라이브러리의 Response 객체.
        """
        self.__content: str = self.__decode_response(resp)
        self.__status: int = resp.status_code

        # 아래 속성은 필요에 따라 활성화 가능
        # self.__content_type: str = resp.headers.get("Content-Type", "").lower()

    def __decode_response(self, resp: requests.Response) -> str:
        """응답 바이트 데이터를 적절한 인코딩으로 디코딩.

        인코딩 정보가 없으면 apparent_encoding, 기본 utf-8 순서로 시도하며,
        UnicodeDecodeError 발생 시 utf-8로 강제 디코딩하고 오류 문자 대체 처리함.

        Args:
            resp (requests.Response): 응답 객체.

        Returns:
            str: 디코딩된 응답 문자열.
        """
        encoding = resp.encoding or resp.apparent_encoding or self.__BASIC_ENCODING
        try:
            return resp.content.decode(encoding)
        except UnicodeDecodeError:
            return resp.content.decode("utf-8", errors="replace")

    def get_content(self) -> str:
        """디코딩된 응답 본문 반환.

        Returns:
            str: 응답 본문.
        """
        return self.__content

    def status(self) -> int:
        """HTTP 상태 코드 반환.

        Returns:
            int: HTTP 상태 코드.
        """
        return self.__status

    # 아래 메서드는 필요에 따라 활성화 가능
    # def content_type(self) -> str:
    #    """Content-Type 헤더 값 반환 (소문자).
    #
    #    Returns:
    #        str: Content-Type 문자열.
    #    """
    #    return self.__content_type

    # 아래 메서드는 필요에 따라 활성화 가능
    # def is_html(self) -> bool:
    #     """응답이 HTML 컨텐츠인지 여부 확인."""
    #     return "html" in self.__content_type

    # def is_xml(self) -> bool:
    #     """응답이 XML 컨텐츠인지 여부 확인."""
    #     return "xml" in self.__content_type

    def is_invalid_response(self) -> bool:
        """응답 내용에 비정상 메시지 포함 여부 판단.

        Returns:
            bool: 비정상 메시지 포함 시 True.
        """
        return any(msg in self.__content for msg in self.__INVALID_RESPONSE_FILTER)
