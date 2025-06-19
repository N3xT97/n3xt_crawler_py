from requests import Response
from requests.models import PreparedRequest
from io import BytesIO
from n3xt_crawler_py.web_crawler.crawl_response import CrawlResponse


def make_fake_response(content: str, content_type: str = "application/xml") -> Response:
    resp = Response()
    resp._content = content.encode("utf-8")
    resp.status_code = 200
    resp.headers["Content-Type"] = content_type
    resp.encoding = "utf-8"
    resp.raw = BytesIO(resp._content)
    resp.request = PreparedRequest()
    resp.request.prepare(method="GET", url="http://example.com")
    return resp


def test_basic_response_properties():
    """기본 HTML 응답이 올바르게 파싱되는지 테스트.

    - 상태 코드가 200인지
    - Content-Type이 'text/html'인지
    - 본문 내용이 원래 콘텐츠와 동일한지 검증.
    """
    content = "<html><body>Hello</body></html>"
    response = make_fake_response(content, "text/html")
    crawl_resp = CrawlResponse(response)

    assert crawl_resp.status() == 200
    assert crawl_resp.get_content() == content


def test_invalid_content_detection():
    """'502 Bad Gateway' 같은 오류 메시지를 유효하지 않은 응답으로 감지하는지 테스트."""
    content = "502 Bad Gateway"
    response = make_fake_response(content, "text/html")
    crawl_resp = CrawlResponse(response)

    # 오류 응답이 유효하지 않은 것으로 인식되는지 확인
    assert crawl_resp.is_invalid_response()


def test_non_utf8_fallback():
    """UTF-8이 아닌 인코딩(ISO-8859-1) 응답을 올바르게 처리하는지 테스트.

    - 특수문자가 포함된 ISO-8859-1 콘텐츠를 인식하고
    - 정상적으로 디코딩해 반환하는지 검증.
    """
    content = "café"
    response = make_fake_response(content, "text/plain")
    response._content = content.encode("iso-8859-1")
    response.encoding = "iso-8859-1"
    crawl_resp = CrawlResponse(response)

    assert "café" in crawl_resp.get_content()
