# LLM 실습 가이드

이 문서는 LLM 프로젝트를 처음부터 실행하는 방법을 단계별로 안내합니다.

## 목차

1. [사전 준비](#사전-준비)
2. [Docker 환경 설정](#docker-환경-설정)
3. [Python 가상 환경 설정](#python-가상-환경-설정)
4. [ChatGPT 스타일 UI 실행](#chatgpt-스타일-ui-실행)
5. [테스트 스크립트 실행](#테스트-스크립트-실행)
6. [트러블슈팅](#트러블슈팅)

---

## 사전 준비

다음 프로그램들이 설치되어 있어야 합니다:

- **Docker Desktop** (Docker & Docker Compose 포함)
  - [macOS 설치 가이드](https://docs.docker.com/desktop/install/mac-install/)
  - [Windows 설치 가이드](https://docs.docker.com/desktop/install/windows-install/)
  - [Linux 설치 가이드](https://docs.docker.com/desktop/install/linux-install/)

- **Python 3.8 이상**
  ```bash
  # Python 버전 확인
  python3 --version
  ```

- **Git** (선택사항, 코드를 clone 하려는 경우)
  ```bash
  # Git 버전 확인
  git --version
  ```

---

## Docker 환경 설정

### 1. Docker Desktop 실행

먼저 Docker Desktop이 실행 중인지 확인합니다.

```bash
# Docker 상태 확인
docker --version
docker-compose --version
```

### 2. Ollama 컨테이너 실행

프로젝트 루트 디렉토리에서 다음 명령어를 실행합니다:

```bash
# Ollama 컨테이너 시작
docker-compose up -d
```

**출력 예시:**
```
[+] Running 2/2
 ✔ Network llm_default  Created
 ✔ Container ollama     Started
```

### 3. 모델 다운로드 확인

Docker Compose가 자동으로 모델을 다운로드합니다. 다음 명령어로 확인할 수 있습니다:

```bash
# 다운로드된 모델 확인
docker exec ollama ollama list
```

**출력 예시:**
```
NAME                   ID              SIZE      MODIFIED
llama2:7b-chat-q4_0    78e26419b446    3.8 GB    2 hours ago
```

### 4. 컨테이너 상태 확인

```bash
# 실행 중인 컨테이너 확인
docker-compose ps
```

**출력 예시:**
```
NAME      IMAGE                  COMMAND               SERVICE   CREATED        STATUS
ollama    ollama/ollama:latest   "/bin/ollama serve"   ollama    5 minutes ago  Up 5 minutes
```

### 5. Ollama 서버 테스트

```bash
# API 엔드포인트 테스트
curl http://localhost:11434/api/tags
```

정상적으로 작동하면 JSON 형식의 모델 정보가 출력됩니다.

---

## Python 가상 환경 설정

### 1. 가상 환경 생성

프로젝트 루트 디렉토리에서:

```bash
# 가상 환경 생성
python3 -m venv venv
```

### 2. 가상 환경 활성화

**macOS / Linux:**
```bash
source venv/bin/activate
```

**Windows (PowerShell):**
```bash
venv\Scripts\Activate.ps1
```

**Windows (CMD):**
```bash
venv\Scripts\activate.bat
```

활성화되면 프롬프트 앞에 `(venv)`가 표시됩니다:
```
(venv) user@machine:~/workspace/llm$
```

### 3. 의존성 패키지 설치

```bash
# requirements.txt 기반으로 패키지 설치
pip install -r requirements.txt
```

**설치되는 패키지:**
- `requests>=2.31.0` - HTTP 클라이언트
- `rich>=13.7.0` - 터미널 UI 라이브러리

### 4. 설치 확인

```bash
# 설치된 패키지 확인
pip list | grep -E "(requests|rich)"
```

---

## ChatGPT 스타일 UI 실행

### 1. 가상 환경 활성화 확인

터미널 프롬프트에 `(venv)`가 표시되는지 확인합니다. 없다면:

```bash
source venv/bin/activate  # macOS/Linux
# 또는
venv\Scripts\activate     # Windows
```

### 2. Chat UI 실행

```bash
python src/chat_ui.py
```

### 3. UI 사용 방법

프로그램이 실행되면 다음과 같은 화면이 표시됩니다:

```
✓ Ollama 서버 연결됨

╭────────────────────────────────── Welcome ───────────────────────────────────╮
│ 🤖 LLM Chat Interface                                                        │
│                                                                              │
│ Ollama 기반 대화형 인터페이스입니다.                                         │
│                                                                              │
│ 명령어                                                                       │
│  • /help - 도움말 표시                                                       │
│  • /history - 대화 기록 보기                                                 │
│  • /clear - 화면 지우기                                                      │
│  • /stats - 세션 통계                                                        │
│  • /quit 또는 /exit - 종료                                                   │
╰──────────────────────────────────────────────────────────────────────────────╯

You ():
```

### 4. 질문하기

프롬프트에 질문을 입력하고 Enter를 누릅니다:

```
You (): 안녕하세요! Python으로 피보나치 수열을 구하는 함수를 작성해주세요.
```

AI가 실시간으로 답변을 스트리밍합니다.

### 5. 명령어 사용

- `/help` - 도움말 보기
- `/history` - 최근 5개 대화 기록 보기
- `/stats` - 세션 통계 (메시지 수, 세션 시간, 토큰 수)
- `/clear` - 화면 지우기
- `/quit` 또는 `/exit` - 프로그램 종료

### 6. 종료

```
You (): /quit
```

또는 `Ctrl+C`를 눌러 종료합니다.

---

## 테스트 스크립트 실행

### Phase 1: Ollama API 기본 테스트

Ollama API의 기본 기능을 테스트합니다.

```bash
# 가상 환경에서 실행
python tests/phase1_ollama_test.py
```

**테스트 내용:**
1. Ollama 서버 연결 테스트
2. 모델 목록 조회
3. 기본 질의/응답 테스트
4. 스트리밍 응답 테스트
5. 성능 측정 (응답 시간, 토큰 수)

### Phase 2: Chain of Thought 테스트

프롬프트 품질과 추론 과정을 테스트합니다.

```bash
# 가상 환경에서 실행
python tests/phase2_cot_test.py
```

**테스트 내용:**
1. 일반 프롬프트 vs CoT 프롬프트 비교
2. 수학 문제 해결 능력 평가
3. 추론 과정의 명확성 확인
4. 응답 품질 비교

---

## 트러블슈팅

### 1. Docker 관련 문제

#### 문제: `Cannot connect to the Docker daemon`
```bash
# Docker Desktop이 실행 중인지 확인
# macOS: Applications에서 Docker Desktop 실행
# Windows: 시작 메뉴에서 Docker Desktop 실행
```

#### 문제: 포트 11434가 이미 사용 중
```bash
# 기존 Ollama 컨테이너 중지
docker-compose down

# 포트 사용 확인 (macOS/Linux)
lsof -i :11434

# 포트 사용 확인 (Windows)
netstat -ano | findstr :11434
```

#### 문제: 모델 다운로드가 안 됨
```bash
# 수동으로 모델 다운로드
docker exec -it ollama ollama pull llama2:7b-chat-q4_0

# 다운로드 진행 상황 확인
docker logs ollama -f
```

### 2. Python 가상 환경 문제

#### 문제: `externally-managed-environment` 에러
```bash
# 시스템 Python 대신 가상 환경 사용 필수
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### 문제: `ModuleNotFoundError: No module named 'requests'`
```bash
# 가상 환경이 활성화되었는지 확인
# 프롬프트에 (venv)가 있어야 함

# 의존성 재설치
pip install -r requirements.txt
```

### 3. Chat UI 실행 문제

#### 문제: `❌ Ollama 서버에 연결할 수 없습니다`
```bash
# 1. Docker 컨테이너 상태 확인
docker-compose ps

# 2. Ollama 컨테이너가 없으면 재시작
docker-compose up -d

# 3. API 엔드포인트 테스트
curl http://localhost:11434/api/tags
```

#### 문제: 질문 시 404 에러 발생
```bash
# 모델 이름 확인
docker exec ollama ollama list

# src/chat_ui.py의 MODEL_NAME이 설치된 모델과 일치하는지 확인
# 현재 설정: llama2:7b-chat-q4_0
```

### 4. 성능 문제

#### 응답이 너무 느림
- **원인**: CPU만 사용하는 경우 응답이 느릴 수 있습니다.
- **해결책**:
  - 더 작은 모델 사용 (예: `llama2:3b`)
  - GPU가 있다면 Ollama GPU 버전 사용
  - 인내심을 갖고 기다리기 (첫 응답은 모델 로딩 시간 포함)

#### 메모리 부족
- **원인**: 7B 모델은 최소 8GB RAM 권장
- **해결책**:
  - 더 작은 모델 사용
  - 다른 프로그램 종료
  - Docker Desktop의 메모리 할당량 증가

### 5. 기타 문제

#### 문제: 한글이 깨져 보임
```bash
# 터미널의 인코딩 설정 확인
# UTF-8로 설정되어 있어야 함

# macOS/Linux
export LANG=ko_KR.UTF-8

# Windows PowerShell
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
```

---

## 다음 단계

1. **Phase 1-2 완료**: 기본 API 테스트와 프롬프트 실험을 완료했다면
2. **Phase 3 시작**: Agent 시스템 구축으로 진행
3. **학습 노트 작성**: `notes/` 디렉토리에 겪은 문제와 해결 과정 기록

더 자세한 정보는 프로젝트 [README.md](../README.md)를 참고하세요.

---

## 도움말

문제가 계속되면:
1. [Ollama 공식 문서](https://github.com/ollama/ollama) 확인
2. GitHub Issues에서 유사한 문제 검색
3. Docker 로그 확인: `docker logs ollama`
4. Python 에러 메시지 전체 내용 확인

**Happy Learning!** 🚀
