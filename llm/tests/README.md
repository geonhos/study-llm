# Tests

LLM 학습 및 실험을 위한 테스트 스크립트 모음

## 파일 구조

- `phase1_ollama_test.py` - Phase 1: Ollama API 기본 테스트
  - Ollama 서버 연결 테스트
  - 모델 다운로드 및 로드 확인
  - 기본 질의/응답 테스트

- `phase2_cot_test.py` - Phase 2: Chain of Thought 프롬프트 테스트
  - 프롬프트 품질 테스트
  - 추론 과정 평가
  - 응답 시간 측정

- `phase2_hallucination_test.py` - Phase 2: Hallucination(환각) 현상 테스트
  - 날조된 정보 생성 여부 확인
  - 잘못된 정보 수정 능력 평가
  - 일관성 및 신뢰성 테스트

## 실행 방법

```bash
# Phase 1 테스트
python3 tests/phase1_ollama_test.py

# Phase 2: Chain of Thought 테스트
python3 tests/phase2_cot_test.py

# Phase 2: Hallucination 테스트
python3 tests/phase2_hallucination_test.py
```

## 요구사항

- Python 3.8+
- Ollama 서버 실행 중 (http://localhost:11434)
- 필요 라이브러리: requests
