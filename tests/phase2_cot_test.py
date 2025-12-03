#!/usr/bin/env python3
"""
Phase 2: Chain of Thought 테스트 스크립트
프롬프트 품질과 한계를 테스트합니다.
"""

import requests
import json
import time
from datetime import datetime

OLLAMA_URL = "http://localhost:11434"
MODEL_NAME = "llama2:7b-chat-q4_0"


def call_llm(prompt, show_response=True):
    """LLM API 호출"""
    url = f"{OLLAMA_URL}/api/generate"

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False
    }

    start_time = time.time()

    try:
        response = requests.post(url, json=payload)
        elapsed_time = time.time() - start_time

        if response.status_code == 200:
            result = response.json()

            if show_response:
                print(f"\n{'='*60}")
                print(f"프롬프트:\n{prompt}")
                print(f"\n{'─'*60}")
                print(f"응답:\n{result['response']}")
                print(f"\n{'─'*60}")
                print(f"⏱️  소요 시간: {elapsed_time:.2f}초")
                print(f"📊 토큰: {result.get('eval_count', 'N/A')} tokens")
                print(f"{'='*60}\n")

            return result, elapsed_time
        else:
            print(f"❌ API 오류: {response.status_code}")
            return None, elapsed_time

    except Exception as e:
        print(f"❌ 예외 발생: {str(e)}")
        return None, time.time() - start_time


# ============================================
# Test 1: 직접 질문 vs Chain of Thought
# ============================================

TEST1_DIRECT = """
한 상점에서 사과를 개당 1,200원에 팔고 있습니다.
오늘 아침 50개가 있었는데, 20개를 팔았고,
오후에 30개를 더 입고받았습니다.
그 후 15개를 더 팔았습니다.
현재 남은 사과의 총 가치는 얼마인가요?

답변만 간단히 작성해주세요.
"""

TEST1_COT = """
한 상점에서 사과를 개당 1,200원에 팔고 있습니다.
오늘 아침 50개가 있었는데, 20개를 팔았고,
오후에 30개를 더 입고받았습니다.
그 후 15개를 더 팔았습니다.
현재 남은 사과의 총 가치는 얼마인가요?

단계별로 생각해봅시다:
1. 먼저 각 단계별 재고를 계산하세요
2. 최종 남은 사과 개수를 구하세요
3. 총 가치를 계산하세요

각 단계를 보여주고 최종 답을 제시해주세요.
"""

# ============================================
# Test 2: 한국어 처리 능력
# ============================================

TEST2_KOREAN = """
다음 문장을 분석해주세요:
"철수는 영희에게 책을 빌려주었다."

누가 책의 원래 주인인가요? 간단히 답해주세요.
"""

# ============================================
# Test 3: Hallucination 테스트
# ============================================

TEST3_FACTUAL = """
2024년 한국의 대통령은 누구인가요?

확실하지 않다면 "모르겠습니다"라고 답해주세요.
"""

# ============================================
# Test 4: 맥락 이해
# ============================================

TEST4_CONTEXT = """
상황: 한 회사에서 LLM을 직접 구축하려고 합니다.

질문: 이 회사가 고려해야 할 가장 중요한 3가지 기술적 어려움은 무엇인가요?

간단히 3가지만 나열해주세요.
"""

# ============================================
# Test 5: 같은 질문 반복 (일관성 테스트)
# ============================================

TEST5_CONSISTENCY = """
9 + 7 = ?

답만 작성해주세요.
"""


def run_test_suite():
    """전체 테스트 실행"""

    print("\n" + "="*60)
    print("Phase 2: 프롬프트 품질 테스트")
    print("="*60)

    results = {}

    # Test 1: Direct vs CoT
    print("\n\n📝 Test 1: 직접 질문 vs Chain of Thought")
    print("─"*60)

    print("\n[1-A] 직접 질문:")
    result_direct, time_direct = call_llm(TEST1_DIRECT)

    print("\n[1-B] Chain of Thought:")
    result_cot, time_cot = call_llm(TEST1_COT)

    results['test1'] = {
        'direct': result_direct,
        'cot': result_cot,
        'time_direct': time_direct,
        'time_cot': time_cot
    }

    # Test 2: 한국어 처리
    print("\n\n📝 Test 2: 한국어 처리 능력")
    print("─"*60)
    result_korean, time_korean = call_llm(TEST2_KOREAN)
    results['test2'] = {'result': result_korean, 'time': time_korean}

    # Test 3: Hallucination
    print("\n\n📝 Test 3: Hallucination 테스트")
    print("─"*60)
    result_factual, time_factual = call_llm(TEST3_FACTUAL)
    results['test3'] = {'result': result_factual, 'time': time_factual}

    # Test 4: 맥락 이해
    print("\n\n📝 Test 4: 맥락 이해")
    print("─"*60)
    result_context, time_context = call_llm(TEST4_CONTEXT)
    results['test4'] = {'result': result_context, 'time': time_context}

    # Test 5: 일관성 (3번 반복)
    print("\n\n📝 Test 5: 일관성 테스트 (3회 반복)")
    print("─"*60)
    consistency_results = []
    for i in range(3):
        print(f"\n[시도 {i+1}/3]")
        result, exec_time = call_llm(TEST5_CONSISTENCY)
        consistency_results.append({
            'result': result,
            'time': exec_time
        })
        time.sleep(1)  # API 부하 방지

    results['test5'] = consistency_results

    # 결과 요약
    print("\n\n" + "="*60)
    print("📊 테스트 요약")
    print("="*60)

    print(f"\nTest 1 - 소요 시간 비교:")
    print(f"  직접 질문: {time_direct:.2f}초")
    print(f"  CoT: {time_cot:.2f}초")
    print(f"  차이: {abs(time_cot - time_direct):.2f}초")

    print(f"\nTest 5 - 일관성:")
    responses = [r['result']['response'].strip() if r['result'] else 'N/A'
                 for r in consistency_results]
    print(f"  응답 1: {responses[0][:50]}...")
    print(f"  응답 2: {responses[1][:50]}...")
    print(f"  응답 3: {responses[2][:50]}...")
    all_same = len(set(responses)) == 1
    print(f"  모두 동일: {'✅' if all_same else '❌'}")

    # 결과 저장
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"test_results_{timestamp}.json"

    with open(filename, 'w', encoding='utf-8') as f:
        # JSON 직렬화 가능하도록 변환
        json_results = {}
        for key, value in results.items():
            if isinstance(value, dict):
                json_results[key] = {
                    k: {
                        'response': v.get('response', '') if isinstance(v, dict) else str(v),
                        'eval_count': v.get('eval_count', 0) if isinstance(v, dict) else 0
                    } if isinstance(v, dict) and 'response' in v else v
                    for k, v in value.items()
                }
            else:
                json_results[key] = value

        json.dump(json_results, f, ensure_ascii=False, indent=2)

    print(f"\n💾 결과 저장: {filename}")

    return results


if __name__ == "__main__":
    print("\n🤖 LLM 프롬프트 테스트 스크립트")
    print("="*60)

    # Ollama 연결 확인
    try:
        response = requests.get(f"{OLLAMA_URL}/api/tags")
        if response.status_code == 200:
            print("✅ Ollama 서버 연결 성공")
        else:
            print("❌ Ollama 서버 응답 오류")
            exit(1)
    except:
        print("❌ Ollama 서버에 연결할 수 없습니다")
        print("   docker-compose up -d 를 실행했는지 확인하세요")
        exit(1)

    # 테스트 실행
    results = run_test_suite()

    print("\n✅ 모든 테스트 완료!")
