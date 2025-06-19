from enum import Enum, auto
import subprocess
import requests
import time
import copy

from n3xt_crawler_py.web_crawler.crawl_url import CrawlUrl
from n3xt_crawler_py.web_crawler.crawl_response import CrawlResponse


class CrawlRequestMode(Enum):
    DEFAULT = auto()
    TOR = auto()


class CrawlRequester:
    __HEADER_FOR_ANTI_ANTI_CRAWLING = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    __MAX_RETRIES = 5
    __TOR_PORT = 9050

    def __init__(
        self, url: CrawlUrl, mode: CrawlRequestMode = CrawlRequestMode.DEFAULT
    ):
        self.__mode: CrawlRequestMode = mode
        self.__resp_data: CrawlResponse = self.__request(url)

    def __is_tor_port_listen(self) -> bool:
        try:
            result = subprocess.run(
                ["netstat", "-na"], capture_output=True, text=True, check=True
            )
        except subprocess.CalledProcessError as e:
            raise RuntimeError(
                f"[{self.__class__.__name__}] Failed to run netstat: {e}"
            )

        for line in result.stdout.splitlines():
            if f"{self.__TOR_PORT}" in line and "LISTEN" in line.upper():
                return True
        return False

    def __set_tor_proxies(self, session: requests.Session) -> requests.Session:
        if not self.__is_tor_port_listen():
            raise RuntimeError(
                f"[{self.__class__.__name__}] Tor mode is enabled but port {self.__TOR_PORT} is not listening."
            )

        proxy_url = f"socks5h://127.0.0.1:{self.__TOR_PORT}"
        session.proxies = {
            "http": proxy_url,
            "https": proxy_url,
        }
        return session

    def __request(self, url: CrawlUrl) -> CrawlResponse:
        session = requests.session()

        if self.__mode == CrawlRequestMode.TOR:
            session = self.__set_tor_proxies(session)

        retries = 0
        while retries < self.__MAX_RETRIES:
            try:
                raw_response = session.get(
                    url.get_url(), headers=self.__HEADER_FOR_ANTI_ANTI_CRAWLING
                )
                response = CrawlResponse(raw_response)
                if response.status() != 200:
                    retries += 1
                    time.sleep(3)
                    continue

                if response.is_invalid_response():
                    retries += 1
                    time.sleep(3)
                    continue

                session.close()
                return response

            except Exception:
                retries += 1
                time.sleep(3)

        session.close()
        raise RuntimeError(
            f"[{self.__class__.__name__}] Failed to get valid response after {self.__MAX_RETRIES} retries."
        )

    def get_response(self) -> CrawlResponse:
        """요청 후 받은 응답 데이터 반환.

        Returns:
            CrawlResponse: 요청 결과.
        """
        return copy.deepcopy(self.__resp_data)
