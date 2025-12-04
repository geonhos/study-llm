# LLM 기초 학습

## 학습 목표

LLM을 직접 실행하고 모델의 품질과 한계를 파악합니다.

**Phase 1-2 학습 내용**:
- Ollama를 통한 로컬 LLM 실행 및 인프라 레벨의 어려움 체험
- 모델 품질 테스트 (Hallucination, 한국어 처리, Chain of Thought 등)
- LLM의 실제 성능과 신뢰성 문제 이해

## 프로젝트 구조

```
llm/
├── src/                   # 소스 코드
│   ├── chat_ui.py        # ChatGPT 스타일 터미널 UI
│   └── __init__.py
├── tests/                 # 테스트 스크립트
│   ├── phase1_ollama_test.py      # Phase 1: Ollama API 기본 테스트
│   ├── phase2_cot_test.py         # Phase 2: Chain of Thought 테스트
│   ├── phase2_hallucination_test.py  # Phase 2: Hallucination 테스트
│   ├── phase2_korean_test.py      # Phase 2: 한국어 처리 테스트
│   ├── __init__.py
│   └── README.md
├── notes/                 # 학습 노트
│   ├── phase1-memory-issue.md
│   ├── phase1-api-test.md
│   ├── phase2-cot-test.md
│   └── phase2-hallucination-test.md
├── docs/                  # 문서
│   └── getting-started.md # 실습 가이드
├── docker-compose.yml     # Ollama 컨테이너 설정
├── requirements.txt       # Python 의존성
└── README.md
```

## 빠른 시작

처음 시작하시는 분은 [실습 가이드](docs/getting-started.md)를 참고하세요.

Docker 실행부터 Chat UI 사용까지 단계별로 안내합니다.

## 환경 설정

### Python 가상 환경 설정

```bash
# 가상 환경 생성 (워크스페이스 루트에서)
python3 -m venv ../venv

# 가상 환경 활성화 (macOS/Linux)
source ../venv/bin/activate

# 가상 환경 활성화 (Windows)
..\venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt
```

### Ollama 실행 (Docker Compose)

```bash
# Ollama 컨테이너 실행
docker-compose up -d

# Llama 2 7B 모델 다운로드 (4-bit 양자화)
docker exec -it ollama ollama pull llama2:7b-chat-q4_0

# 모델 실행 테스트
docker exec -it ollama ollama run llama2:7b-chat-q4_0
```

### 컨테이너 관리

```bash
# 컨테이너 중지
docker-compose down

# 로그 확인
docker-compose logs -f
```

### ChatGPT 스타일 터미널 UI 실행

```bash
# 가상 환경 활성화 (먼저 위의 가상 환경 설정 완료 필요)
source ../venv/bin/activate

# ChatGPT 스타일 인터페이스 실행
python src/chat_ui.py
```

**주요 기능:**
- 🎨 Rich 라이브러리 기반 아름다운 터미널 UI
- 💬 실시간 스트리밍 응답
- 📜 대화 히스토리 관리
- 📊 세션 통계 (메시지 수, 토큰 수, 세션 시간)
- 🎯 마크다운 렌더링 지원

**명령어:**
- `/help` - 도움말
- `/history` - 대화 기록
- `/stats` - 세션 통계
- `/clear` - 화면 지우기
- `/quit` - 종료

## 학습 내용

### Phase 1: LLM 직접 실행해보기

**목표**: LLM을 직접 구동하면서 인프라 레벨의 어려움 파악

**완료된 항목**:
- [x] Ollama로 Llama 2 7B 모델 로컬 실행
- [x] 모델 다운로드 크기 및 시간 측정
- [x] 메모리/CPU 사용량 모니터링
- [x] 응답 속도(latency) 측정 및 분석

**주요 발견사항**:
- 모델 크기: 7B 파라미터 모델도 4-8GB 이상 메모리 필요
- GPU vs CPU: 응답 속도 차이 (초 단위 vs 분 단위)
- 모델 로딩 시간: Cold start 문제
- 참고: [Phase 1 노트](notes/)

### Phase 2: 모델 품질과 한계 파악

**목표**: LLM의 실제 성능과 신뢰성 문제 이해

**완료된 항목**:
- [x] Chain of Thought (CoT) 테스트
- [x] Hallucination(환각) 현상 확인
- [x] 한국어 처리 능력 평가

**주요 발견사항**:
- 답변의 일관성: 같은 질문에 다른 답변
- 사실 확인: 잘못된 정보 생성 가능성
- 한국어 품질: 영어 대비 성능 차이
- 컨텍스트 제한: 긴 대화나 문서 처리의 한계
- 참고: [Phase 2 노트](notes/)

## 학습 자료

### 추천 강의
- Andrej Karpathy - Neural Networks: Zero to Hero
- DeepLearning.AI - ChatGPT Prompt Engineering for Developers
- Fast.ai - Practical Deep Learning for Coders

### 추천 도서
- "Hands-On Large Language Models" - Jay Alammar & Maarten Grootendorst
- "Build a Large Language Model (From Scratch)" - Sebastian Raschka

### 유용한 링크
- [Ollama Documentation](https://github.com/ollama/ollama)
- [Hugging Face Models](https://huggingface.co/models)
- [LangChain Documentation](https://python.langchain.com/)
- [Prompt Engineering Guide](https://www.promptingguide.ai/)

## 구현 내용

### CLI 기반 Chat UI
- ChatGPT 스타일 터미널 인터페이스
- 실시간 스트리밍 응답
- 대화 히스토리 관리
- 세션 통계 (메시지 수, 토큰 수, 세션 시간)

### 테스트 스크립트
- Ollama API 기본 테스트
- Chain of Thought (CoT) 테스트
- Hallucination 현상 테스트
- 한국어 처리 능력 테스트

## 학습 노트

### 직접 겪은 문제점과 해결 과정
실습하면서 마주친 구체적인 어려움들을 `notes/` 디렉토리에 기록했습니다.

- [Phase 1: 메모리 부족 문제](notes/phase1-memory-issue.md)
- [Phase 1: API 테스트 결과](notes/phase1-api-test.md)
- [Phase 2: Chain of Thought 테스트](notes/phase2-cot-test.md)
- [Phase 2: Hallucination 현상 테스트](notes/phase2-hallucination-test.md)

### 주요 학습 내용

**인프라 레벨의 어려움**:
- 모델 크기와 메모리 요구사항
- CPU/GPU 리소스 관리
- 응답 속도와 레이턴시

**모델 품질과 한계**:
- Hallucination 현상
- 한국어 처리 품질
- 컨텍스트 길이 제한
- 답변의 일관성 문제

---

**학습 기간**: 2025-12-02 ~ 2025-12-04
