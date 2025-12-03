#!/usr/bin/env python3
"""
Ollama API 테스트 스크립트
Ollama API를 통해 LLM과 질의/응답을 테스트합니다.
"""

import requests
import json
import time

# Ollama API 엔드포인트
OLLAMA_URL = "http://localhost:11434"
MODEL_NAME = "llama2:7b-chat-q4_0"


def check_ollama_status():
    """Ollama 서버 상태 확인"""
    try:
        response = requests.get(f"{OLLAMA_URL}/api/tags")
        if response.status_code == 200:
            print("✓ Ollama 서버 실행 중")
            models = response.json().get("models", [])
            if models:
                print(f"✓ 사용 가능한 모델: {len(models)}개")
                for model in models:
                    print(f"  - {model['name']} (크기: {model['size'] / (1024**3):.2f} GB)")
                return True
            else:
                print("✗ 다운로드된 모델 없음")
                return False
        else:
            print(f"✗ Ollama 서버 응답 오류: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("✗ Ollama 서버에 연결할 수 없습니다")
        return False


def generate_response(prompt, show_metrics=True):
    """
    Ollama API로 질의하고 응답 받기

    Args:
        prompt: 질의 내용
        show_metrics: 성능 메트릭 표시 여부
    """
    url = f"{OLLAMA_URL}/api/generate"

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False  # 스트리밍 비활성화
    }

    print(f"\n{'='*60}")
    print(f"질문: {prompt}")
    print(f"{'='*60}")

    start_time = time.time()

    try:
        response = requests.post(url, json=payload)

        if response.status_code == 200:
            result = response.json()
            elapsed_time = time.time() - start_time

            # 응답 출력
            print(f"\n답변:\n{result['response']}")

            # 메트릭 출력
            if show_metrics:
                print(f"\n{'─'*60}")
                print("📊 성능 메트릭:")
                print(f"  - 총 소요 시간: {elapsed_time:.2f}초")
                print(f"  - 생성된 토큰 수: {result.get('eval_count', 'N/A')}")
                print(f"  - 프롬프트 토큰 수: {result.get('prompt_eval_count', 'N/A')}")

                if result.get('eval_count') and result.get('total_duration'):
                    tokens_per_sec = result['eval_count'] / (result['total_duration'] / 1e9)
                    print(f"  - 토큰 생성 속도: {tokens_per_sec:.2f} tokens/sec")

                print(f"  - 모델 로딩 시간: {result.get('load_duration', 0) / 1e9:.2f}초")
                print(f"{'─'*60}")

            return result
        else:
            print(f"\n✗ API 오류: {response.status_code}")
            print(f"내용: {response.text}")
            return None

    except Exception as e:
        print(f"\n✗ 예외 발생: {str(e)}")
        return None


def chat_streaming(prompt):
    """
    스트리밍 방식으로 응답 받기 (실시간 출력)

    Args:
        prompt: 질의 내용
    """
    url = f"{OLLAMA_URL}/api/generate"

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": True  # 스트리밍 활성화
    }

    print(f"\n{'='*60}")
    print(f"질문: {prompt}")
    print(f"{'='*60}\n")
    print("답변: ", end="", flush=True)

    start_time = time.time()

    try:
        response = requests.post(url, json=payload, stream=True)

        if response.status_code == 200:
            full_response = ""

            for line in response.iter_lines():
                if line:
                    chunk = json.loads(line)
                    if 'response' in chunk:
                        text = chunk['response']
                        print(text, end="", flush=True)
                        full_response += text

                    if chunk.get('done', False):
                        elapsed_time = time.time() - start_time
                        print(f"\n\n{'─'*60}")
                        print(f"📊 총 소요 시간: {elapsed_time:.2f}초")
                        print(f"{'─'*60}")
                        break

            return full_response
        else:
            print(f"\n✗ API 오류: {response.status_code}")
            return None

    except Exception as e:
        print(f"\n✗ 예외 발생: {str(e)}")
        return None


def interactive_mode():
    """대화형 모드"""
    print("\n" + "="*60)
    print("대화형 모드 (종료하려면 'quit' 또는 'exit' 입력)")
    print("="*60)

    while True:
        try:
            prompt = input("\n질문: ").strip()

            if prompt.lower() in ['quit', 'exit', 'q']:
                print("종료합니다.")
                break

            if not prompt:
                continue

            chat_streaming(prompt)

        except KeyboardInterrupt:
            print("\n\n종료합니다.")
            break


def run_test_queries():
    """테스트 질의 실행"""
    test_prompts = [
        "What is Python?",
        "Explain machine learning in one sentence.",
        "2 + 2는 얼마인가요?"
    ]

    print("\n" + "="*60)
    print("테스트 질의 실행")
    print("="*60)

    for prompt in test_prompts:
        result = generate_response(prompt, show_metrics=True)
        time.sleep(1)  # API 부하 방지를 위한 대기


def main():
    """메인 함수"""
    print("\n🤖 Ollama API 테스트 스크립트")
    print("="*60)

    # 서버 상태 확인
    if not check_ollama_status():
        print("\n⚠️  먼저 Ollama 서버를 실행하고 모델을 다운로드하세요:")
        print("  docker-compose up -d")
        print("  docker exec ollama ollama pull llama2:7b-chat-q4_0")
        return

    # 메뉴 선택
    print("\n선택하세요:")
    print("  1. 테스트 질의 실행")
    print("  2. 대화형 모드")
    print("  3. 종료")

    choice = input("\n선택 (1-3): ").strip()

    if choice == "1":
        run_test_queries()
    elif choice == "2":
        interactive_mode()
    else:
        print("종료합니다.")


if __name__ == "__main__":
    main()
