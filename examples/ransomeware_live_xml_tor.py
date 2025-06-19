from typing import Dict, Tuple

# 크롤링 관련 클래스 및 유틸리티 모듈 임포트
from n3xt_crawler_py.data_processor.crawl_data_process_manager import (
    CrawlDataProcessManager,
    ICrawlDataProcessor,
)
from n3xt_crawler_py.web_crawler.crawl_client import CrawlClient
from n3xt_crawler_py.web_crawler.crawl_requester import CrawlRequestMode
from n3xt_crawler_py.data_parser.crawl_parser import CrawlParseMode
from n3xt_crawler_py.utils.crawl_save import save_dict_list_as_file


# 데이터 후처리기 정의: RSS title 필드만 추출
class RsTitleProcessor(ICrawlDataProcessor):

    def __init__(self, unique_id: str):
        super().__init__()  # 인터페이스 초기화
        self.__unique_id: str = unique_id

    # 데이터를 받아서 title 필드 가공
    def run(self, data: Dict) -> Tuple[str, str]:
        try:
            raw_title = data["title"][0]  # 첫 번째 title 요소 가져오기
            title = raw_title[5:]  # 앞의 불필요한 문자열 제거
        except IndexError:
            title = ""  # title이 없을 경우 빈 문자열 반환
        return self.get_unique_id(), title

    # 고유 이름 반환 (저장 시 키 이름으로 사용)
    def get_unique_id(self) -> str:
        return self.__unique_id


# 크롤링 클라이언트 생성
client = CrawlClient(
    "https://www.ransomware.live/rss.xml", CrawlRequestMode.TOR, CrawlParseMode.XML
)

# 필드 추출
extracted = client.extract_fields(
    block_xpath="//item",
    fields_map={
        "title": ".//title/text()",
    },
)

# 후처리기 매니저에 커스텀 Processor 등록
process_manager = CrawlDataProcessManager()
process_manager.add(RsTitleProcessor(unique_id="title"))

# 파싱된 데이터에 후처리기 적용
ransomeware_live = []
for raw_data in extracted:
    processed_data = process_manager.run_all(raw_data)  # title 필드 가공
    ransomeware_live.append(processed_data)

# 결과 저장
file_name = save_dict_list_as_file(ransomeware_live, "data/ransome")

# 저장 완료 메시지 출력
print(f"'{file_name}' saved")
