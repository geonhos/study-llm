#!/usr/bin/env python3
"""
Phase 2: 한국어 처리 능력 평가 테스트

LLM의 한국어 이해 및 생성 능력을 다각도로 테스트합니다.
"""

import requests
import json
import time
from datetime import datetime

# Ollama API 설정
OLLAMA_URL = "http://localhost:11434"
MODEL_NAME = "llama2:7b-chat-q4_0"


def generate_response(prompt: str, temperature: float = 0.7) -> dict:
    """LLM 응답 생성"""
    url = f"{OLLAMA_URL}/api/generate"

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": temperature
        }
    }

    start_time = time.time()
    response = requests.post(url, json=payload, timeout=300)
    elapsed = time.time() - start_time

    if response.status_code == 200:
        data = response.json()
        return {
            "success": True,
            "response": data.get("response", ""),
            "elapsed_time": elapsed,
            "eval_count": data.get("eval_count", 0),
            "total_duration": data.get("total_duration", 0)
        }
    else:
        return {
            "success": False,
            "error": f"HTTP {response.status_code}",
            "elapsed_time": elapsed
        }


def print_section(title: str):
    """섹션 헤더 출력"""
    print("\n" + "="*80)
    print(f"  {title}")
    print("="*80 + "\n")


def print_test_result(test_name: str, prompt: str, result: dict, analysis: str = ""):
    """테스트 결과 출력"""
    print(f"📝 테스트: {test_name}")
    print(f"   질문: {prompt}")
    print(f"   응답 시간: {result['elapsed_time']:.2f}초")

    if result['success']:
        print(f"\n   응답:")
        print(f"   {'-'*70}")
        # 응답을 줄바꿈하여 출력
        response_lines = result['response'].strip().split('\n')
        for line in response_lines:
            print(f"   {line}")
        print(f"   {'-'*70}")

        if analysis:
            print(f"\n   분석: {analysis}")
    else:
        print(f"   ❌ 오류: {result['error']}")

    print()


def test_basic_korean_understanding():
    """1. 기본 한국어 이해 능력"""
    print_section("1. 기본 한국어 이해 능력")

    tests = [
        {
            "name": "간단한 인사",
            "prompt": "안녕하세요? 저는 LLM 학습을 하고 있습니다. 당신은 무엇을 도와줄 수 있나요?",
            "analysis": "기본적인 한국어 인사와 질문 이해"
        },
        {
            "name": "설명 요청",
            "prompt": "인공지능이 무엇인지 간단하게 설명해주세요.",
            "analysis": "한국어로 개념 설명 요청"
        },
        {
            "name": "비교 질문",
            "prompt": "머신러닝과 딥러닝의 차이점은 무엇인가요?",
            "analysis": "한국어로 된 비교 질문 이해"
        }
    ]

    results = []
    for test in tests:
        result = generate_response(test["prompt"])
        print_test_result(test["name"], test["prompt"], result, test["analysis"])
        results.append({
            "test": test["name"],
            "prompt": test["prompt"],
            "response": result.get("response", ""),
            "analysis": test["analysis"]
        })

    return results


def test_complex_sentences():
    """2. 복잡한 한국어 문장 이해"""
    print_section("2. 복잡한 한국어 문장 이해")

    tests = [
        {
            "name": "긴 문장",
            "prompt": "제가 최근에 읽은 책에서는 인공지능 기술이 발전하면서 우리 사회의 여러 분야에서 큰 변화가 일어나고 있으며, 특히 의료, 교육, 금융 등의 영역에서 혁신적인 서비스들이 등장하고 있다고 설명하고 있는데, 이러한 변화가 우리 일상 생활에 미치는 긍정적인 영향은 무엇일까요?",
            "analysis": "긴 복문 구조의 한국어 이해"
        },
        {
            "name": "이중 부정",
            "prompt": "인공지능이 인간을 대체하지 않을 수 없다는 주장에 반대하지 않는 사람들의 의견은 무엇인가요?",
            "analysis": "이중 부정 표현의 이해"
        },
        {
            "name": "피동/사동 표현",
            "prompt": "데이터가 수집되고 분석되어 결과가 도출되는 과정을 설명해주세요.",
            "analysis": "피동형 표현의 이해"
        }
    ]

    results = []
    for test in tests:
        result = generate_response(test["prompt"])
        print_test_result(test["name"], test["prompt"], result, test["analysis"])
        results.append({
            "test": test["name"],
            "prompt": test["prompt"],
            "response": result.get("response", ""),
            "analysis": test["analysis"]
        })

    return results


def test_korean_culture_knowledge():
    """3. 한국 문화 및 역사 지식"""
    print_section("3. 한국 문화 및 역사 지식")

    tests = [
        {
            "name": "한국 역사",
            "prompt": "세종대왕의 업적 중 가장 중요한 것은 무엇인가요?",
            "expected": "훈민정음(한글) 창제",
            "analysis": "한국 역사에 대한 지식"
        },
        {
            "name": "한국 명절",
            "prompt": "추석에는 어떤 음식을 먹고 무엇을 하나요?",
            "expected": "송편, 성묘, 차례",
            "analysis": "한국 전통 명절에 대한 이해"
        },
        {
            "name": "한국 지리",
            "prompt": "한국의 수도는 어디이며, 한국에서 가장 높은 산은 무엇인가요?",
            "expected": "서울, 한라산 또는 백두산",
            "analysis": "한국 지리에 대한 지식"
        },
        {
            "name": "한국 문화",
            "prompt": "김치는 어떻게 만들며, 한국인의 식생활에서 어떤 의미가 있나요?",
            "expected": "발효 음식, 반찬",
            "analysis": "한국 음식 문화에 대한 이해"
        }
    ]

    results = []
    for test in tests:
        result = generate_response(test["prompt"])
        print_test_result(
            test["name"],
            test["prompt"],
            result,
            f"{test['analysis']} (기대 답변: {test['expected']})"
        )
        results.append({
            "test": test["name"],
            "prompt": test["prompt"],
            "response": result.get("response", ""),
            "expected": test["expected"],
            "analysis": test["analysis"]
        })

    return results


def test_korean_generation_quality():
    """4. 한국어 생성 품질"""
    print_section("4. 한국어 생성 품질")

    tests = [
        {
            "name": "자연스러운 문장 생성",
            "prompt": "Python 프로그래밍을 배우고 싶은 초보자에게 조언을 해주세요. (한국어로 답변해주세요)",
            "analysis": "자연스러운 한국어 문장 생성 능력"
        },
        {
            "name": "기술 용어 설명",
            "prompt": "클라우드 컴퓨팅을 초등학생도 이해할 수 있게 한국어로 설명해주세요.",
            "analysis": "쉬운 한국어로 기술 개념 설명"
        },
        {
            "name": "창의적 글쓰기",
            "prompt": "AI와 인간이 함께 일하는 미래에 대해 짧은 이야기를 한국어로 써주세요.",
            "analysis": "창의적인 한국어 글쓰기"
        }
    ]

    results = []
    for test in tests:
        result = generate_response(test["prompt"])
        print_test_result(test["name"], test["prompt"], result, test["analysis"])
        results.append({
            "test": test["name"],
            "prompt": test["prompt"],
            "response": result.get("response", ""),
            "analysis": test["analysis"]
        })

    return results


def test_korean_english_mixed():
    """5. 한영 혼용 처리"""
    print_section("5. 한영 혼용 텍스트 처리")

    tests = [
        {
            "name": "Konglish 이해",
            "prompt": "머신러닝 모델을 트레이닝할 때 오버피팅을 방지하는 방법은 무엇인가요?",
            "analysis": "한영 혼용 기술 용어 이해"
        },
        {
            "name": "영어 단어 설명",
            "prompt": "API가 무엇인지 한국어로 설명하고, RESTful API의 특징도 알려주세요.",
            "analysis": "영어 약어를 한국어로 설명"
        },
        {
            "name": "코드와 한국어 혼용",
            "prompt": "Python에서 list comprehension을 사용하는 방법을 한국어로 설명하고 예제 코드를 보여주세요.",
            "analysis": "프로그래밍 용어와 한국어 혼용"
        }
    ]

    results = []
    for test in tests:
        result = generate_response(test["prompt"])
        print_test_result(test["name"], test["prompt"], result, test["analysis"])
        results.append({
            "test": test["name"],
            "prompt": test["prompt"],
            "response": result.get("response", ""),
            "analysis": test["analysis"]
        })

    return results


def test_formal_informal_speech():
    """6. 존댓말/반말 구분"""
    print_section("6. 존댓말/반말 구분")

    tests = [
        {
            "name": "존댓말 요청",
            "prompt": "인공지능의 미래에 대해 존댓말로 설명해주세요.",
            "analysis": "존댓말 사용 능력"
        },
        {
            "name": "반말 요청",
            "prompt": "인공지능의 미래에 대해 친구에게 말하듯이 편하게 설명해줘.",
            "analysis": "반말 사용 능력"
        },
        {
            "name": "격식 있는 표현",
            "prompt": "회사 보고서에 들어갈 내용으로 AI 기술 도입의 필요성을 작성해주세요.",
            "analysis": "격식 있는 문체 사용"
        }
    ]

    results = []
    for test in tests:
        result = generate_response(test["prompt"])
        print_test_result(test["name"], test["prompt"], result, test["analysis"])
        results.append({
            "test": test["name"],
            "prompt": test["prompt"],
            "response": result.get("response", ""),
            "analysis": test["analysis"]
        })

    return results


def test_idioms_and_proverbs():
    """7. 관용어 및 속담 이해"""
    print_section("7. 한국어 관용어 및 속담 이해")

    tests = [
        {
            "name": "속담 의미",
            "prompt": "'백지장도 맞들면 낫다'는 속담의 의미는 무엇인가요?",
            "expected": "협력, 팀워크",
            "analysis": "한국 속담의 의미 이해"
        },
        {
            "name": "관용어 사용",
            "prompt": "'발등에 불이 떨어졌다'는 표현은 어떤 상황을 말하나요?",
            "expected": "긴급한 상황",
            "analysis": "한국어 관용어 이해"
        },
        {
            "name": "사자성어",
            "prompt": "'일석이조(一石二鳥)'의 뜻과 사용 예시를 알려주세요.",
            "expected": "한 가지 행동으로 두 가지 이익",
            "analysis": "사자성어 이해"
        }
    ]

    results = []
    for test in tests:
        result = generate_response(test["prompt"])
        print_test_result(
            test["name"],
            test["prompt"],
            result,
            f"{test['analysis']} (기대: {test['expected']})"
        )
        results.append({
            "test": test["name"],
            "prompt": test["prompt"],
            "response": result.get("response", ""),
            "expected": test["expected"],
            "analysis": test["analysis"]
        })

    return results


def test_context_understanding():
    """8. 맥락 이해 능력"""
    print_section("8. 맥락 이해 능력 (Multi-turn)")

    print("다음은 연속된 질문으로 맥락을 유지하는 능력을 테스트합니다.\n")

    # 첫 번째 질문
    prompt1 = "서울에서 부산까지 가는 방법을 알려주세요."
    print(f"질문 1: {prompt1}")
    result1 = generate_response(prompt1)
    if result1['success']:
        print(f"응답 1: {result1['response'][:200]}...")
        print(f"응답 시간: {result1['elapsed_time']:.2f}초\n")

    # 두 번째 질문 (맥락 참조)
    prompt2 = "그 중에서 가장 빠른 방법은 무엇인가요?"
    print(f"질문 2: {prompt2}")
    result2 = generate_response(prompt2)
    if result2['success']:
        print(f"응답 2: {result2['response'][:200]}...")
        print(f"응답 시간: {result2['elapsed_time']:.2f}초\n")

    # 세 번째 질문 (대명사 참조)
    prompt3 = "그것의 소요 시간과 비용은 얼마나 되나요?"
    print(f"질문 3: {prompt3}")
    result3 = generate_response(prompt3)
    if result3['success']:
        print(f"응답 3: {result3['response'][:200]}...")
        print(f"응답 시간: {result3['elapsed_time']:.2f}초\n")

    print("분석: 이전 맥락을 참조하는 대명사('그 중에서', '그것의')를 올바르게 이해하는지 확인")
    print("참고: Stateless API 호출이므로 맥락을 유지하지 못할 가능성이 높음\n")

    return [
        {"prompt": prompt1, "response": result1.get("response", "")},
        {"prompt": prompt2, "response": result2.get("response", "")},
        {"prompt": prompt3, "response": result3.get("response", "")}
    ]


def main():
    """메인 함수"""
    print("\n" + "="*80)
    print("  Phase 2: 한국어 처리 능력 평가 테스트")
    print("="*80)
    print(f"\n모델: {MODEL_NAME}")
    print(f"시작 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    all_results = {}

    # 1. 기본 한국어 이해
    all_results['basic'] = test_basic_korean_understanding()

    # 2. 복잡한 문장 이해
    all_results['complex'] = test_complex_sentences()

    # 3. 한국 문화/역사 지식
    all_results['culture'] = test_korean_culture_knowledge()

    # 4. 한국어 생성 품질
    all_results['generation'] = test_korean_generation_quality()

    # 5. 한영 혼용 처리
    all_results['mixed'] = test_korean_english_mixed()

    # 6. 존댓말/반말 구분
    all_results['formality'] = test_formal_informal_speech()

    # 7. 관용어/속담 이해
    all_results['idioms'] = test_idioms_and_proverbs()

    # 8. 맥락 이해
    all_results['context'] = test_context_understanding()

    # 요약
    print_section("테스트 완료")
    print(f"종료 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"\n📊 총 {len(all_results)} 카테고리의 한국어 처리 능력 테스트를 완료했습니다.")
    print(f"\n결과 분석:")
    print(f"1. 기본 이해: {len(all_results.get('basic', []))}개 테스트")
    print(f"2. 복잡한 문장: {len(all_results.get('complex', []))}개 테스트")
    print(f"3. 문화/역사: {len(all_results.get('culture', []))}개 테스트")
    print(f"4. 생성 품질: {len(all_results.get('generation', []))}개 테스트")
    print(f"5. 한영 혼용: {len(all_results.get('mixed', []))}개 테스트")
    print(f"6. 격식 수준: {len(all_results.get('formality', []))}개 테스트")
    print(f"7. 관용어/속담: {len(all_results.get('idioms', []))}개 테스트")
    print(f"8. 맥락 이해: {len(all_results.get('context', []))}회 대화")
    print(f"\n💡 각 응답을 검토하여 LLM이:")
    print(f"   - 한국어를 정확하게 이해하는지")
    print(f"   - 자연스러운 한국어를 생성하는지")
    print(f"   - 한국 문화/역사를 올바르게 설명하는지")
    print(f"   - 존댓말/반말을 구분하는지")
    print(f"   - 한국어 관용어와 속담을 이해하는지")
    print(f"   확인이 필요합니다.\n")

    return all_results


if __name__ == "__main__":
    try:
        results = main()
        print("✅ 테스트가 성공적으로 완료되었습니다.")
    except KeyboardInterrupt:
        print("\n\n⚠️  사용자에 의해 테스트가 중단되었습니다.")
    except Exception as e:
        print(f"\n❌ 오류 발생: {str(e)}")
