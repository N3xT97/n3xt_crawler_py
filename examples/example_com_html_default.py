from typing import Dict, Tuple

from n3xt_crawler_py.data_processor.crawl_data_process_manager import (
    CrawlDataProcessManager,
    ICrawlDataProcessor,
)
from n3xt_crawler_py.web_crawler.crawl_client import CrawlClient
from n3xt_crawler_py.web_crawler.crawl_requester import CrawlRequestMode
from n3xt_crawler_py.data_parser.crawl_parser import CrawlParseMode
from n3xt_crawler_py.utils.crawl_save import save_dict_list_as_file


# 데이터 후처리기 정의: 'title' 항목만 추출
class ExTextProcessor(ICrawlDataProcessor):

    def __init__(self, unique_id: str):
        super().__init__()  # 부모 인터페이스 초기화
        self.__unique_id: str = unique_id

    # 각 데이터 블록에서 title 항목 추출
    def run(self, data: Dict) -> Tuple[str, str]:
        try:
            title = data["text"][0]  # 첫 번째 title 텍스트 추출
        except IndexError:
            title = ""  # 데이터가 없을 경우 빈 문자열 반환
        return self.get_unique_id(), title

    # 고유 키 이름 반환
    def get_unique_id(self) -> str:
        return self.__unique_id


# 크롤링 클라이언트 생성
client = CrawlClient(
    "https://example.com", CrawlRequestMode.DEFAULT, CrawlParseMode.HTML
)

# 필드 추출
extracted = client.extract_fields(
    block_xpath="/html/body/div/p",
    fields_map={
        "text": ".//text()",
    },
)

# 후처리 프로세스 매니저 생성 및 후처리 프로세서 등록
processor_manager = CrawlDataProcessManager()
processor_manager.add(ExTextProcessor(unique_id="text"))

# 크롤링된 데이터 후처리
example_com = []
for raw_data in extracted:
    processed_data = processor_manager.run_all(raw_data)  # {"text": "..."}
    example_com.append(processed_data)

# 결과 데이터를 파일로 저장
file_name = save_dict_list_as_file(example_com, "data/example")

# 완료 메시지 출력
print(f"'{file_name}' saved")
