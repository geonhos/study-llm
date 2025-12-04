# LLM & Agent Study

## 개요

LLM과 AI Agent를 실무적인 관점에서 학습하고 실험하는 프로젝트입니다.

**학습 목표**: "회사에 LLM/Agent를 직접 구축하기 힘든 이유"를 실습을 통해 이해하기

## 프로젝트 구조

```
workspace/llm/
├── llm/                    # LLM 기초 학습 (Phase 1-2 완료)
│   ├── src/               # Chat UI 구현
│   ├── tests/             # LLM 품질 테스트
│   ├── notes/             # 학습 노트
│   └── docs/              # 문서
├── agent/                  # Agent 학습 (진행 예정)
└── venv/                  # Python 가상 환경
```

## 학습 단계

### ✅ Phase 1-2: LLM 기초 (완료)
**위치**: `llm/` 디렉토리

로컬에서 LLM을 직접 실행하고 모델의 품질과 한계를 파악했습니다.

**주요 내용**:
- Ollama를 통한 Llama 2 7B 모델 실행
- 인프라 레벨의 어려움 체험 (메모리, CPU, 응답 속도)
- 모델 품질 테스트 (Hallucination, 한국어 처리, CoT)
- ChatGPT 스타일 터미널 UI 구현

**상세 내용**: [llm/README.md](llm/README.md)

### 🚀 Phase 3+: Agent 시스템 (진행 예정)
**위치**: `agent/` 디렉토리

LLM 기반 Agent 시스템을 구축하면서 엔지니어링 복잡도를 체감합니다.

**계획된 내용**:
- Agent 아키텍처 설계
- Tool/Function Calling 구현
- Multi-turn 대화 및 상태 관리
- RAG (Retrieval-Augmented Generation)
- 프로덕션 레벨 고려사항

## 환경 설정

### Python 가상 환경

```bash
# 가상 환경 생성
python3 -m venv venv

# 가상 환경 활성화 (macOS/Linux)
source venv/bin/activate

# 가상 환경 활성화 (Windows)
venv\Scripts\activate
```

### 각 프로젝트 실행

각 디렉토리의 README를 참고하세요:
- LLM 기초: [llm/README.md](llm/README.md)
- Agent: [agent/README.md](agent/README.md) (작성 예정)

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

## 학습 일정

- **2025-12-02 ~ 2025-12-04**: LLM 기초 (Phase 1-2) - ✅ 완료
- **2025-12-04 ~**: Agent 시스템 (Phase 3+) - 🚀 시작 예정

---

**주요 발견사항**

LLM을 직접 구축하고 운영하는 것은 생각보다 훨씬 어렵습니다:

1. **인프라 비용**: 7B 모델도 최소 4-8GB 메모리 필요, GPU 없이는 실용적인 응답 속도 불가능
2. **품질 관리**: Hallucination, 일관성, 한국어 품질 등 예측하기 어려운 문제들
3. **엔지니어링 복잡도**: 상태 관리, 에러 처리, 컨텍스트 관리 등 추가적인 엔지니어링 필요

실무에서는 OpenAI, Anthropic 같은 API 서비스를 사용하는 것이 훨씬 효율적일 수 있습니다.
