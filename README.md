# LLM Study

## 학습 목표

**"회사에 LLM을 직접 구축하기 힘든 이유"**를 실습을 통해 이해하기

직접 LLM을 실행하고 Agent를 구축하는 과정에서:
- 얼마나 많은 노력과 신경이 필요한지
- 어떤 기술적 처리들이 요구되는지
- 실제 프로덕션 환경에서 고려해야 할 사항들은 무엇인지

실무 관점에서 파악하고 정리합니다.

## 환경 설정

### Ollama 실행 (Docker Compose)

```bash
# Ollama 컨테이너 실행
docker-compose up -d

# Llama 2 7B 모델 다운로드
docker exec -it ollama ollama pull llama2:7b

# 모델 실행 테스트
docker exec -it ollama ollama run llama2:7b
```

### 컨테이너 관리

```bash
# 컨테이너 중지
docker-compose down

# 로그 확인
docker-compose logs -f
```

## 학습 로드맵

### Phase 1: LLM 직접 실행해보기

**목표**: LLM을 직접 구동하면서 인프라 레벨의 어려움 파악

- [ ] Ollama로 Llama 2 7B 모델 로컬 실행
- [ ] 모델 다운로드 크기 및 시간 측정
- [ ] 메모리/CPU 사용량 모니터링
- [ ] 응답 속도(latency) 측정 및 분석
- [ ] 여러 요청 동시 처리 시 성능 변화 관찰

**고려해야 할 포인트**:
- 모델 크기: 7B 파라미터 모델도 4-8GB 이상 메모리 필요
- GPU vs CPU: 응답 속도 차이 (초 단위 vs 분 단위)
- 동시성 처리: 멀티 유저 환경에서 리소스 관리
- 모델 로딩 시간: Cold start 문제
- 스케일링: 트래픽 증가 시 인프라 비용

### Phase 2: 모델 품질과 한계 파악

**목표**: LLM의 실제 성능과 신뢰성 문제 이해

- [ ] 다양한 프롬프트로 응답 품질 테스트
- [ ] Hallucination(환각) 현상 확인
- [ ] 한국어 처리 능력 평가
- [ ] 도메인 특화 질문에 대한 정확도 측정
- [ ] Temperature, Top-p 등 파라미터 튜닝

**고려해야 할 포인트**:
- 답변의 일관성: 같은 질문에 다른 답변
- 사실 확인: 잘못된 정보 생성 가능성
- 편향성: 학습 데이터의 편향이 답변에 반영
- 컨텍스트 제한: 긴 대화나 문서 처리의 한계
- 최신 정보 부재: 학습 시점 이후 정보 부족

### Phase 3: Agent 시스템 구축

**목표**: LLM 기반 Agent를 만들면서 엔지니어링 복잡도 체감

- [ ] LangChain 또는 직접 구현으로 기본 Agent 구조 설계
- [ ] Tool/Function Calling 구현
- [ ] Multi-turn 대화 상태 관리
- [ ] 메모리/컨텍스트 관리 시스템
- [ ] 에러 핸들링 및 재시도 로직

**고려해야 할 포인트**:
- 상태 관리: 대화 히스토리, 컨텍스트 유지
- 에러 복구: LLM 응답 실패 시 처리
- 비용 추정: API 호출 횟수 * 토큰 수
- 응답 파싱: LLM 출력의 비정형성 처리
- 디버깅 난이도: 비결정적 동작으로 재현 어려움

### Phase 4: RAG (Retrieval-Augmented Generation) 구현

**목표**: 실시간 정보 활용을 위한 추가 시스템 구축 경험

- [ ] Vector Database 선택 및 설정 (ChromaDB, Pinecone 등)
- [ ] 문서 임베딩 및 저장
- [ ] 유사도 검색 및 컨텍스트 구성
- [ ] RAG 파이프라인 통합
- [ ] 검색 품질 평가 및 개선

**고려해야 할 포인트**:
- 추가 인프라: Vector DB, 임베딩 모델 필요
- 데이터 동기화: 최신 정보 업데이트 전략
- 검색 정확도: Retrieval 품질이 답변에 직접 영향
- 레이턴시 증가: 검색 + LLM 호출의 누적 시간
- 청크 전략: 문서 분할 방식에 따른 성능 차이

### Phase 5: 프로덕션 레벨 고려사항

**목표**: 실제 서비스 운영 시 필요한 요소들 파악

- [ ] 로깅 및 모니터링 시스템
- [ ] Rate limiting 및 큐 관리
- [ ] 응답 캐싱 전략
- [ ] 사용자 입력 검증 및 필터링
- [ ] 비용 추적 및 최적화

**고려해야 할 포인트**:
- 보안: Prompt injection, 민감 정보 노출
- 비용 관리: 예상치 못한 과금 폭탄
- 가용성: 모델 서버 다운타임 대응
- 규정 준수: 데이터 보관, 개인정보 처리
- 책임성: AI 생성 결과에 대한 법적 책임

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

## 실습 프로젝트

각 Phase를 완료하면서 단계적으로 구현할 프로젝트

### 프로젝트 목표
간단한 업무 자동화 Agent를 만들면서 실제 구축 시 마주치는 문제점들을 체험

### 프로젝트 구성
1. **Phase 1-2**: CLI 기반 질의응답 시스템
   - 기본적인 LLM 호출 및 응답 처리
   - 성능 메트릭 수집 (응답 시간, 메모리 사용량)

2. **Phase 3**: 도구를 사용하는 Agent
   - 날씨 조회, 계산기, 웹 검색 등 외부 도구 연동
   - 멀티턴 대화 및 상태 관리

3. **Phase 4**: RAG 기반 문서 QA
   - 회사 문서/매뉴얼 검색 및 답변
   - 검색 품질 및 답변 정확도 평가

4. **Phase 5**: 프로덕션 준비
   - API 서버화 (FastAPI)
   - 모니터링 대시보드
   - 비용 및 성능 리포트

## 학습 노트

### 직접 겪은 문제점과 해결 과정
실습하면서 마주친 구체적인 어려움들을 `notes/` 디렉토리에 기록합니다.

- [Phase 1: 메모리 부족 문제](notes/phase1-memory-issue.md)
- [Phase 1: API 테스트 결과](notes/phase1-api-test.md)

### 구축의 어려움 정리
"회사에 LLM을 직접 구축하기 힘든 이유"를 실무 관점에서 정리합니다.

#### 기술적 측면
- [ ] 인프라 리소스 요구사항
- [ ] 성능과 비용의 트레이드오프
- [ ] 엔지니어링 복잡도

#### 운영적 측면
- [ ] 품질 보증의 어려움
- [ ] 유지보수 부담
- [ ] 보안 및 규정 준수

#### 비즈니스 측면
- [ ] 개발 및 운영 인력
- [ ] 총 소유 비용 (TCO)
- [ ] 시장 솔루션과의 비교

---

**시작일**: 2025-12-02
