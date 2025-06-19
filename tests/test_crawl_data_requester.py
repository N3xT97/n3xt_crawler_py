from n3xt_crawler_py.web_crawler.crawl_url import CrawlUrl
from n3xt_crawler_py.web_crawler.crawl_requester import CrawlRequester
from n3xt_crawler_py.web_crawler.crawl_url import CrawlUrl


def test_real_request():
    """실제 HTTP 요청을 보내고 응답 콘텐츠를 확인하는 테스트.

    - URL에 요청을 보낸 후
    - 응답 본문이 문자열인지
    - 'Example Domain'이라는 텍스트가 포함되어 있는지 확인.
    """
    url = CrawlUrl("https://www.example.com")
    requester = CrawlRequester(url)

    # 실제 요청을 보내고 콘텐츠를 가져옴
    content = requester.get_response().get_content()

    assert isinstance(content, str)
    assert "Example Domain" in content
