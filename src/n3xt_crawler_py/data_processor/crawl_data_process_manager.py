from abc import ABC, abstractmethod
from typing import Any, Dict, Tuple, List


class ICrawlDataProcessor(ABC):
    """크롤링 데이터 후처리를 위한 인터페이스 클래스입니다.

    모든 데이터 프로세서는 고유 이름을 가져야 하며,
    입력 데이터를 받아 (키, 값) 쌍으로 결과를 반환해야 합니다.
    """

    @abstractmethod
    def run(self, data: Any) -> Tuple[Any, Any]:
        """입력 데이터를 처리하여 결과를 반환합니다.

        Args:
            data (Any): 원시 입력 데이터.

        Returns:
            Tuple[Any, Any]: (결과를 저장할 키, 처리된 값)
        """
        pass

    @abstractmethod
    def get_unique_id(self) -> Any:
        """프로세서를 구별할 수 있는 고유 이름을 반환합니다.

        Returns:
            Any: 프로세서의 고유 식별자.
        """
        pass


class CrawlDataProcessManager:
    """복수의 데이터 프로세서를 실행하고 결과를 병합하는 매니저 클래스."""

    def __init__(self):
        """프로세서 목록 초기화."""
        self.__processor_set: List[ICrawlDataProcessor] = []

    def add(self, processor: ICrawlDataProcessor) -> None:
        """프로세서를 매니저에 등록합니다.

        고유 이름이 중복될 경우 ValueError를 발생시킵니다.

        Args:
            processor (ICrawlDataProcessor): 등록할 데이터 프로세서.

        Raises:
            ValueError: 이미 동일한 이름의 프로세서가 등록된 경우.
        """
        existing_names = {p.get_unique_id() for p in self.__processor_set}
        proc_id = processor.get_unique_id()

        if proc_id in existing_names:
            cls = self.__class__.__name__
            raise ValueError(f"[{cls}] Processor with name '{proc_id}' already exists.")

        self.__processor_set.append(processor)

    def run_all(self, data: Any) -> Dict[Any, Any]:
        """등록된 모든 프로세서를 실행하고 결과를 병합해 반환합니다.

        각 프로세서의 결과는 고유 키로 구분되어 반환됩니다.

        Args:
            data (Any): 입력 데이터.

        Returns:
            Dict[Any, Any]: 프로세서별 처리 결과 딕셔너리.

        Raises:
            RuntimeError: 등록된 프로세서가 없는 경우.
            KeyError: 서로 다른 프로세서가 동일한 키를 반환한 경우.
        """
        if not self.__processor_set:
            cls = self.__class__.__name__
            raise RuntimeError(
                f"[{cls}] No processors registered. Add at least one before running."
            )

        result: Dict[Any, Any] = {}

        for processor in self.__processor_set:
            key, value = processor.run(data)
            if key in result:
                cls = self.__class__.__name__
                raise KeyError(f"[{cls}] Duplicate key returned by processor: '{key}'")
            result[key] = value

        return result
