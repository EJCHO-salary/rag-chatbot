# RAG Chatbot (No-Vector BM25)

이 프로젝트는 벡터 임베딩 대신 키워드 기반 검색(BM25)을 사용하는 RAG(Retrieval-Augmented Generation) 챗봇입니다. 로컬 파일(PDF, TXT, MD)과 웹 페이지의 내용을 학습하고, 이를 바탕으로 사용자의 질문에 답변합니다.

이 프로젝트는 **Harness Engineering** ([https://github.com/EJCHO-salary/harnessEngineering](https://github.com/EJCHO-salary/harnessEngineering))에 의해 자율적으로 구축된 첫 번째 프로젝트입니다.

## 주요 기능

- **문서 로딩**: PDF, TXT, MD 파일 및 웹 URL의 텍스트를 추출하고 청크(chunk) 단위로 분할합니다.
- **BM25 검색**: 고성능 키워드 매칭 알고리즘인 `rank-bm25`를 사용하여 관련성 높은 문서를 검색합니다.
- **LLM 통합**: `litellm`을 통해 Google Gemini 등 다양한 LLM 모델과 연동합니다.
- **대화형 CLI**: `rich` 라이브러리를 사용한 세련된 터미널 인터페이스를 제공합니다.
- **로컬 스토리지**: 검색 인덱스를 JSON 형태로 로컬에 저장하여 재사용할 수 있습니다.

## 아키텍처 개요

1. **수집(Ingestion)**: 파일이나 URL에서 텍스트를 읽어 `data/chunks.json`에 저장합니다.
2. **검색(Retrieval)**: 사용자의 질문과 가장 유사한 키워드를 가진 상위 5개의 텍스트 청크를 찾습니다.
3. **생성(Generation)**: 검색된 청크와 사용자의 질문을 LLM에 전달하여 답변을 생성합니다.

## 기술 스택

- **언어**: Python 3.12+
- **패키지 관리**: `uv`
- **검색 엔진**: `rank-bm25`
- **LLM Interface**: `litellm` (Default: Gemini 1.5 Flash)
- **CLI**: `typer`, `rich`
- **문서 처리**: `pypdf`, `beautifulsoup4`, `httpx`

## 설치 방법

이 프로젝트는 `uv`를 사용하여 의존성을 관리합니다.

1. 저장소를 클론합니다:
   ```bash
   git clone <repository-url>
   cd rag-chatbot
   ```

2. 의존성을 동기화합니다:
   ```bash
   uv sync
   ```

## 환경 설정

프로젝트 루트 디렉토리에 `.env` 파일을 생성하고 필요한 API 키를 설정합니다.

```env
GEMINI_API_KEY=your_gemini_api_key_here
LLM_MODEL=gemini/gemini-1.5-flash
DATA_DIR=data
```

## 사용법

`uv run` 명령어를 사용하여 CLI를 실행할 수 있습니다.

### 1. 데이터 로드 및 인덱싱

로컬 파일, 디렉토리 또는 웹 URL을 인덱싱합니다.

```bash
# 단일 파일 로드
uv run -m ragchat.cli load ./documents/sample.pdf

# 디렉토리 전체 로드 (txt, md, pdf 지원)
uv run -m ragchat.cli load ./documents/

# 웹 페이지 로드
uv run -m ragchat.cli load https://example.com/article
```

### 2. 챗봇과 대화하기

인덱싱된 데이터를 바탕으로 질문을 던집니다.

```bash
uv run -m ragchat.cli chat
```

`exit` 또는 `quit`을 입력하여 대화를 종료할 수 있습니다.

## 프로젝트 구조

```text
rag-chatbot/
├── src/
│   └── ragchat/
│       ├── loader.py       # 문서 및 파일 로딩 로직
│       ├── search.py       # BM25 검색 구현
│       ├── web.py          # 웹 크롤링 로직
│       ├── llm.py          # LiteLLM 래퍼
│       ├── chat.py         # 메인 대화 루프
│       ├── cli.py          # Typer/CLI 엔트리포인트
│       └── config.py       # 설정 및 환경 변수
├── data/                   # 인덱스 및 청크 저장소 (JSON)
└── pyproject.toml          # 프로젝트 설정 및 의존성
```

---
*Built autonomously by Harness Engineering.*
