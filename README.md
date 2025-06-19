# 📦 crawler 설치 및 개발 가이드

본 프로젝트는 [Poetry](https://python-poetry.org/) 기반으로 관리되는 크롤러 패키지입니다. 아래 설명을 따라 로컬 설치, 가상환경 실행, 테스트 및 TOR 모드 사용이 가능합니다.

## 🔧 1. 로컬 설치 방법

`pyproject.toml`이 있는 디렉토리에서 아래 명령어 중 하나를 실행하세요.

| 명령어                | 설명                                | 설치 방식              | 사용 목적            |
|---------------------|-----------------------------------|---------------------|-------------------|
| `pip install .`     | 현재 폴더를 패키지로 설치                   | **복사하여 설치**         | 사용자 환경 / 배포용     |
| `pip install -e .`  | 현재 폴더를 개발용 패키지로 설치 (코드 자동 반영) | **심볼릭 링크 (editable)** | 개발 중 사용          |

> 💡 설치된 패키지를 제거하려면:  
> `pip uninstall n3xt_crawler_py`

## 🧪 2. Poetry 가상환경 사용

이 프로젝트는 Poetry로 관리되며, 아래와 같은 명령어로 개발, 테스트, 의존성 관리를 할 수 있습니다.

### 📥 설치 및 의존성 관리

| 명령어                            | 설명                                        | 설치 방식                     |
|--------------------------------|-------------------------------------------|----------------------------|
| `poetry install`               | 의존성 설치 및 소스 패키지 등록                      | 심볼릭 링크 (editable)         |
| `poetry add package_name`      | PyPI 패키지를 의존성에 추가 및 설치                | PyPI에서 다운로드            |
| `poetry add --editable ./path` | 로컬 패키지를 개발 모드로 의존성 추가                | 심볼릭 링크 (editable)         |
| `poetry update`                | 모든 의존성을 최신 버전으로 업그레이드                | `poetry.lock` 파일 갱신 포함   |

### ▶️ 가상환경에서 예제 실행 (예: `examples/` 폴더)

| 목적                       | 명령어                                                    |
|--------------------------|-----------------------------------------------------------|
| 예제 스크립트 실행             | `poetry run python examples/your_script.py`              |
| 출력 지연 방지 (unbuffered) | `poetry run python -u examples/your_script.py`           |
| 로그 파일로 출력 저장         | `poetry run python examples/your_script.py > output.log 2>&1` |

### 🧪 가상환경에서 테스트 실행 (예: `tests/` 폴더)

| 목적                         | 명령어                                                    |
|----------------------------|-----------------------------------------------------------|
| 전체 테스트 실행                | `poetry run pytest`                                       |
| 출력 버퍼링 없이 실행           | `poetry run pytest -s`                                    |
| 특정 테스트 파일 실행           | `poetry run pytest tests/test_example.py`                 |
| 실패 시 자세한 출력             | `poetry run pytest -v`                                    |
| 테스트 로그 저장               | `poetry run pytest > test_output.log 2>&1`                |

## 🕵️ 3. TOR 모드 사용

TOR 브라우저를 통해 익명성 확보가 필요한 크롤링을 수행할 수 있습니다.

### 🪟 Windows

- Tor 브라우저 설치 후, 설치 폴더 내 `tor.exe` 실행  
  예: `C:\Tor Browser\Browser\TorBrowser\Tor\tor.exe`

### 🐧 Linux

- `tor` 패키지를 설치하고 서비스 실행  
  ```bash
  sudo apt install tor
  sudo service tor start

> 📌 Tor 연결 상태 확인은 9050 포트를 통해 socks 프록시로 요청을 보내 테스트할 수 있습니다.

## 📄 기타

* 모든 명령은 프로젝트 루트 디렉토리(`pyproject.toml` 위치)에서 실행하세요.
* Poetry가 설치되어 있지 않다면 [설치 가이드](https://python-poetry.org/docs/#installation)를 참고하세요.

</br></br></br>

# 🕷️ `CrawlClient` 사용법 가이드

`CrawlClient`는 주어진 URL에서 데이터를 요청하고, XPath로 필요한 필드를 추출하는 작업을 간단하게 처리할 수 있습니다.

## 📦 주요 클래스: `CrawlClient`

```python
class CrawlClient:
    def __init__(self, url: str, req_mode: CrawlRequestMode, parse_mode: CrawlParseMode)
```

* `url`: 크롤링할 웹 페이지 주소
* `req_mode`: 요청 방식 (`DEFAULT`, `TOR`, 등)
* `parse_mode`: HTML 파싱 방식 (`HTML`, `XML`, 등)

## 🧪 기본 사용 예제

```python
from n3xt_crawler_py.web_crawler.crawl_client import CrawlClient
from n3xt_crawler_py.web_crawler.crawl_requester import CrawlRequestMode
from n3xt_crawler_py.data_parser.crawl_parser import CrawlParseMode

# 크롤링 대상 웹 페이지
url = "https://example.com"

# CrawlClient 인스턴스 생성
client = CrawlClient(
    url=url,
    req_mode=CrawlRequestMode.DEFAULT,
    parse_mode=CrawlParseMode.HTML
)

# 특정 XPath 블록에서 텍스트 필드 추출
results = client.extract_fields(
    block_xpath="/html/body/div/p",  # 반복되는 블록 단위
    fields_map={
        "text": ".//text()",         # 블록 내부에서 텍스트 추출
    }
)

for item in results:
    print(item)
```

## 📘 `extract_fields()` 설명

```python
def extract_fields(
    block_xpath: str,
    fields_map: Dict[str, str],
) -> List[Dict[str, List[str]]]:
```

* `block_xpath`: 반복되는 데이터 블록을 지정 (예: 게시글 하나, 카드 하나 등)
* `fields_map`: 추출할 필드 이름과 해당 XPath

예시 반환값:

```python
[
    {"text": ["Example Text 1"]},
    {"text": ["Example Text 2"]},
]
```

## 📌 결과 형식

* 반환값은 항상 `List[Dict[str, List[str]]]` 형태입니다.
* 각 블록(`block_xpath`) 단위로 반복되며, 필드별로 리스트로 결과가 담깁니다.

```python
[
    {
        "title": ["Example"], 
        "link": ["https://example.com"]
    },
    {
        "title": ["Second"], 
        "link": ["https://example.org"]
    },
]
```

## 🛠 추가 팁

* XPath의 상대 경로(`./`, `.//`)는 `block_xpath` 기준 블록 내부를 기준으로 작성해야 합니다.
* HTML 파싱 시 잘못된 태그 구조도 자동으로 보정됩니다 (`lxml.html` 사용).
* 중첩된 블록, 다수의 필드 추출 등 복잡한 구조도 대응 가능.

</br></br></br>

# 📘 CrawlDataProcessorManager 사용법

## 📄 개요

`CrawlDataProcessorManager`는 여러 개의 데이터 처리기(processor)를 등록하고, 입력 데이터를 각 처리기에 전달하여 결과를 병합해 반환하는 유틸리티 클래스입니다.

`ICrawlDataProcessor`는 처리기들이 구현해야 하는 인터페이스로, 고유 이름과 실행 메서드를 정의합니다.

## ✅ 클래스 정의

```python
class ICrawlDataProcessor(ABC):
    def run(self, data: Dict) -> Tuple[str, Any]:
        """입력 데이터를 처리하고 (키, 값) 쌍을 반환합니다."""
        pass

    def get_unique_id(self) -> str:
        """프로세서를 고유하게 식별할 수 있는 이름을 반환합니다."""
        pass
```

```python
class CrawlDataProcessorManager:
    def add(self, processor: ICrawlDataProcessor) -> None:
        """프로세서를 매니저에 등록합니다. 이름이 중복되면 ValueError 발생."""
        pass

    def run_all(self, raw: Dict) -> Dict[str, Any]:
        """등록된 모든 프로세서를 실행하고 결과를 병합해 반환합니다.

        Raises:
            RuntimeError: 프로세서가 하나도 등록되지 않은 경우
            KeyError: 동일한 키를 반환하는 프로세서가 둘 이상인 경우
        """
        pass
```

## 🧩 인터페이스 구현 예시

```python
class MyProcessor(ICrawlDataProcessor):
    def __init__(self, unique: str):
        self.__unique = unique

    def run(self, data: Dict) -> Tuple[str, Any]:
        # 예: raw에서 'value' 키를 꺼내 제곱하여 반환
        value = data.get("value", 0)
        return self.__unique, value ** 2

    def get_unique_id(self) -> str:
        return self.__unique
```

## 🧩 매니저 사용 예시

```python
# 매니저 생성
manager = CrawlDataProcessManager()

# 프로세서 등록
manager.add(MyProcessor("square"))
manager.add(MyProcessor("square2"))

# 입력 데이터 준비
raw_data = {"value": 5}

# 모든 프로세서 실행
result = manager.run_all(raw_data)

print(result)
# 출력: {'square': 25, 'square2': 25}
```

## ⚠️ 예외 처리

* `ValueError`: 같은 이름의 프로세서를 등록하려고 할 경우
* `RuntimeError`: 아무 프로세서도 등록하지 않고 `run_all()`을 호출한 경우
* `KeyError`: 서로 다른 프로세서가 동일한 키를 반환한 경우

## 🛠 활용 사례

* 크롤링한 데이터의 후처리(정제, 필터링, 요약 등)를 다단계로 수행
* 다양한 포맷(텍스트, 메타데이터 등)에 대한 독립적인 처리 모듈 구성
* 파이프라인 확장 시 단일 인터페이스로 일관된 로직 유지 가능

