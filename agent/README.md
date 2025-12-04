# API Documentation Agent

## 프로젝트 개요

API 문서를 기반으로 개발에 필요한 코드와 데이터를 자동 생성해주는 LLM Agent

## 최종 목표

**API 문서 기반 자동 생성 Agent 구축**

입력: API 문서 (OpenAPI/Swagger, RESTful API 문서 등)

출력:
- cURL 커맨드
- Java HTTP Request 코드
- Request/Response 모델 클래스
- 샘플 JSON 데이터
- API 사용 예제 코드

## 학습 계획

### Phase 1: Agent 프레임워크 학습

**LangChain 기초**
- [ ] LLM 체인 구성 (Prompt → LLM → Output Parser)
- [ ] Memory 관리 (대화 히스토리, 컨텍스트 유지)
- [ ] Agent & Tools (Function Calling, ReAct 패턴)
- [ ] Document Loaders & Text Splitters

**LlamaIndex 기초**
- [ ] Index 구조 이해 (VectorStoreIndex, ListIndex 등)
- [ ] Query Engine 활용
- [ ] Document Processing
- [ ] LangChain vs LlamaIndex 비교 및 선택

**실습 프로젝트**
- 간단한 문서 Q&A Agent
- Tool을 사용하는 ReAct Agent
- 대화형 멀티턴 Agent

### Phase 2: RAG 시스템 구축

**목표**: API 문서를 효과적으로 검색하고 활용

- [ ] Vector DB 선택 및 설정 (ChromaDB/FAISS)
- [ ] API 문서 임베딩 전략
- [ ] 유사도 검색 및 컨텍스트 구성
- [ ] Retrieval 품질 개선

**실습**
- API 문서 임베딩 및 저장
- 질문에 맞는 API 엔드포인트 검색
- 검색 결과 기반 답변 생성

### Phase 3: API 문서 파싱 및 이해

**목표**: 다양한 형식의 API 문서 처리

- [ ] OpenAPI/Swagger 스펙 파싱
- [ ] RESTful API 문서 구조 분석
- [ ] 엔드포인트, 파라미터, 응답 형식 추출
- [ ] 문서 정규화 및 구조화

**실습**
- Swagger JSON/YAML 파서 구현
- API 문서 → 구조화된 데이터 변환
- 다양한 문서 형식 지원

### Phase 4: 코드 생성 Agent 구현

**목표**: API 문서 기반 자동 코드 생성

**기능 구현**
- [ ] cURL 커맨드 생성기
- [ ] Java HTTP Request 생성기 (OkHttp, RestTemplate 등)
- [ ] Request/Response DTO 클래스 생성
- [ ] 샘플 JSON 데이터 생성
- [ ] API 사용 예제 코드 생성

**Agent 설계**
- [ ] Tool 정의 (각 생성 기능별)
- [ ] Prompt Engineering (정확한 코드 생성)
- [ ] 출력 검증 및 포맷팅
- [ ] 에러 처리 및 재시도 로직

**실습**
- 실제 API 문서로 테스트
- 생성된 코드 검증
- 사용성 개선

### Phase 5: 프로덕션 레벨 고도화

**목표**: 실무에서 사용 가능한 수준으로 개선

- [ ] CLI 인터페이스 구현
- [ ] 배치 처리 (여러 API 동시 처리)
- [ ] 템플릿 커스터마이징
- [ ] 설정 파일 관리
- [ ] 로깅 및 에러 리포팅

## 기술 스택

### Core
- **LLM**: OpenAI GPT-4 or Anthropic Claude
- **Agent Framework**: LangChain / LlamaIndex
- **Vector DB**: ChromaDB or FAISS

### Tools
- **API Parsing**: PyYAML, openapi-spec-validator
- **Code Generation**: Jinja2 (템플릿), ast (코드 검증)
- **HTTP Client**: requests (테스트용)

### Development
- **Language**: Python 3.10+
- **Testing**: pytest
- **CLI**: Click or Typer

## 프로젝트 구조 (예정)

```
agent/
├── src/
│   ├── agents/              # Agent 구현
│   │   ├── api_agent.py    # 메인 Agent
│   │   └── tools/          # Agent Tools
│   ├── parsers/            # API 문서 파서
│   ├── generators/         # 코드 생성기
│   │   ├── curl.py
│   │   ├── java.py
│   │   └── json.py
│   └── rag/                # RAG 시스템
├── tests/                  # 테스트
├── examples/               # 예제 API 문서
├── templates/              # 코드 템플릿
├── docs/                   # 학습 노트
└── README.md
```

## 참고 자료

### 공식 문서
- [LangChain Documentation](https://python.langchain.com/)
- [LlamaIndex Documentation](https://docs.llamaindex.ai/)
- [OpenAPI Specification](https://swagger.io/specification/)

### 학습 자료
- LangChain 공식 튜토리얼
- LlamaIndex Quickstart
- Building Production-Ready RAG Applications

## 예상 결과물

입력 예시:
```yaml
/users/{id}:
  get:
    summary: Get user by ID
    parameters:
      - name: id
        in: path
        required: true
        schema:
          type: integer
    responses:
      200:
        description: Success
        content:
          application/json:
            schema:
              type: object
              properties:
                id: integer
                name: string
                email: string
```

출력 예시:
```bash
# cURL
curl -X GET "https://api.example.com/users/123" \
     -H "Content-Type: application/json"

# Java (OkHttp)
// UserResponse.java
public class UserResponse {
    private Integer id;
    private String name;
    private String email;
    // getters, setters...
}

// API Call
Request request = new Request.Builder()
    .url("https://api.example.com/users/123")
    .get()
    .build();
```

