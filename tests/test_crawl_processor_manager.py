import pytest
from n3xt_crawler_py.data_processor.crawl_data_process_manager import (
    CrawlDataProcessManager,
    ICrawlDataProcessor,
)


class DummyProcessor(ICrawlDataProcessor):
    def __init__(self, unique_name: str):
        self.__unique_name = unique_name

    def run(self, data: dict):
        return self.__unique_name, f"value_of_{self.__unique_name}"

    def get_unique_id(self):
        return self.__unique_name


def test_add_and_run_all_success():
    """여러 프로세서를 등록하고 모두 정상적으로 실행되는지 테스트."""
    manager = CrawlDataProcessManager()
    p1 = DummyProcessor("proc1")
    p2 = DummyProcessor("proc2")

    # 프로세서 두 개를 매니저에 추가
    manager.add(p1)
    manager.add(p2)

    # 빈 raw 데이터를 입력으로 실행
    raw = {}
    result = manager.run_all(raw)

    # 각 프로세서의 결과가 키-값으로 포함되어야 함
    assert result == {
        "proc1": "value_of_proc1",
        "proc2": "value_of_proc2",
    }


def test_add_duplicate_processor_name_should_raise():
    """같은 이름의 프로세서를 두 번 추가하면 예외가 발생해야 함."""
    manager = CrawlDataProcessManager()
    p1 = DummyProcessor("proc1")
    p2 = DummyProcessor("proc1")  # 이름이 중복됨

    manager.add(p1)

    # 두 번째 추가 시 ValueError가 발생해야 함
    with pytest.raises(ValueError) as e:
        manager.add(p2)

    assert "already exists" in str(e.value)


def test_run_all_without_processors_should_raise():
    """등록된 프로세서가 없는 상태에서 실행하면 예외가 발생해야 함."""
    manager = CrawlDataProcessManager()

    # 아무 프로세서도 추가하지 않은 상태에서 run_all 호출
    with pytest.raises(RuntimeError) as e:
        manager.run_all({})

    assert "No processors registered" in str(e.value)


def test_run_all_with_duplicate_key_should_raise():
    """여러 프로세서가 동일한 키를 반환할 경우 예외가 발생해야 함."""

    # run()이 동일한 키를 반환하도록 재정의된 프로세서
    class ConflictProcessor(DummyProcessor):
        def run(self, data):
            return "conflict_key", "value"

    manager = CrawlDataProcessManager()
    p1 = ConflictProcessor("proc1")
    p2 = ConflictProcessor("proc2")

    manager.add(p1)
    manager.add(p2)

    # 중복 키가 발생하므로 KeyError가 발생해야 함
    with pytest.raises(KeyError) as e:
        manager.run_all({})

    assert "Duplicate key" in str(e.value)
