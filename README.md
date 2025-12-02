# LLM Study

LLM(Large Language Model) 학습을 위한 저장소입니다.

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

## 학습 스케줄

### Week 1-2: LLM 기초 이해
- [ ] LLM의 개념과 역사 학습
- [ ] Transformer 아키텍처 이해
- [ ] Attention Mechanism 개념 정리
- [ ] Ollama 환경 설정 및 기본 사용법 익히기
- [ ] Prompt Engineering 기초

### Week 3-4: 모델 실습
- [ ] Llama 2 7B 모델로 기본 프롬프트 실습
- [ ] 다양한 프롬프트 패턴 테스트
- [ ] Temperature, Top-p 등 파라미터 실험
- [ ] Few-shot Learning 예제 작성
- [ ] Chain of Thought 프롬프팅 연습

### Week 5-6: 고급 활용
- [ ] RAG (Retrieval-Augmented Generation) 개념 학습
- [ ] Vector Database 이해 (ChromaDB, Pinecone 등)
- [ ] LangChain 기초 학습
- [ ] 간단한 챗봇 애플리케이션 구현
- [ ] Function Calling 실습

### Week 7-8: 실전 프로젝트
- [ ] 개인 프로젝트 아이디어 선정
- [ ] 프로젝트 설계 및 구현
- [ ] 성능 최적화 및 튜닝
- [ ] 프로젝트 문서화
- [ ] 학습 내용 정리 및 회고

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

## 프로젝트 아이디어

1. **개인 문서 QA 시스템**: RAG를 활용한 개인 문서 검색 및 질의응답
2. **코드 리뷰 어시스턴트**: 코드 분석 및 개선 제안 도구
3. **학습 노트 요약기**: 긴 문서를 자동으로 요약하는 도구
4. **다국어 번역 챗봇**: 실시간 번역 및 대화 지원
5. **SQL 쿼리 생성기**: 자연어를 SQL로 변환하는 도구

## 학습 노트

학습하면서 배운 내용들을 정리합니다.

### 진행 중인 학습
- 진행 상황을 여기에 기록합니다.

---

**시작일**: 2025-12-02
