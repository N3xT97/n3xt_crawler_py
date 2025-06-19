import re


class CrawlUrl:
    """URL 문자열을 검증하고 저장하는 클래스.

    생성 시 URL 형식이 유효한지 정규식으로 검사합니다.

    Attributes:
        __URL_RE (str): URL 형식을 검증하기 위한 정규식 패턴.
        __url (str): 검증된 URL 문자열.
    """

    __URL_RE = r"(?:https?:\/\/)?(?:www\.)?([a-zA-Z0-9-]+\.[a-zA-Z0-9-]+\.[a-zA-Z]{2,}|[a-zA-Z0-9-]+\.[a-zA-Z]{2,})(?=\/|$)"

    def __init__(self, url: str):
        """CrawlUrl 객체 생성자.

        Args:
            url (str): 검사하고 저장할 URL 문자열.

        Raises:
            ValueError: URL 형식이 유효하지 않은 경우 발생.
        """
        if not self.__is_url(url):
            raise ValueError(f"[{self.__class__.__name__}] Invalid URL format: '{url}'")

        self.__url = url

    def __is_url(self, url: str) -> bool:
        """주어진 문자열이 URL 형식에 맞는지 검사.

        Args:
            url (str): 검사할 문자열.

        Returns:
            bool: 형식이 올바르면 True, 아니면 False.
        """
        return re.search(self.__URL_RE, url) is not None

    def get_url(self) -> str:
        """저장된 URL 문자열 반환.

        Returns:
            str: 저장된 URL.
        """
        return self.__url
