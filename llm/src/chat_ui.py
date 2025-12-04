#!/usr/bin/env python3
"""
ChatGPT 스타일 터미널 UI
Rich 라이브러리를 사용한 인터랙티브 채팅 인터페이스
"""

import requests
import json
import time
from datetime import datetime
from typing import Optional, List, Dict

from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.live import Live
from rich.spinner import Spinner
from rich.table import Table
from rich.prompt import Prompt
from rich.layout import Layout
from rich.text import Text
from rich import box

# Ollama API 설정
OLLAMA_URL = "http://localhost:11434"
MODEL_NAME = "llama2:7b-chat-q4_0"

console = Console()


class ChatSession:
    """채팅 세션 관리"""

    def __init__(self):
        self.history: List[Dict[str, str]] = []
        self.start_time = datetime.now()

    def add_message(self, role: str, content: str, tokens: Optional[int] = None):
        """메시지 추가"""
        self.history.append({
            "role": role,
            "content": content,
            "timestamp": datetime.now(),
            "tokens": tokens
        })

    def get_history_text(self) -> str:
        """히스토리를 텍스트로 변환"""
        if not self.history:
            return "[dim]대화 기록이 없습니다.[/dim]"

        text = ""
        for msg in self.history[-5:]:  # 최근 5개만 표시
            time_str = msg["timestamp"].strftime("%H:%M:%S")
            role_emoji = "👤" if msg["role"] == "user" else "🤖"
            text += f"[dim]{time_str}[/dim] {role_emoji} "
            if msg["role"] == "user":
                text += f"[cyan]{msg['content'][:50]}...[/cyan]\n" if len(msg['content']) > 50 else f"[cyan]{msg['content']}[/cyan]\n"
            else:
                text += f"[green]{msg['content'][:50]}...[/green]\n" if len(msg['content']) > 50 else f"[green]{msg['content']}[/green]\n"

        return text

    def get_stats(self) -> Table:
        """세션 통계"""
        table = Table(box=box.SIMPLE, show_header=False, padding=(0, 1))
        table.add_column(style="cyan")
        table.add_column(style="green")

        duration = datetime.now() - self.start_time
        total_tokens = sum(msg.get("tokens", 0) for msg in self.history)

        table.add_row("💬 총 메시지", str(len(self.history)))
        table.add_row("⏱️  세션 시간", f"{duration.seconds // 60}분 {duration.seconds % 60}초")
        table.add_row("🎯 토큰 수", str(total_tokens) if total_tokens > 0 else "N/A")

        return table


def check_ollama_connection() -> bool:
    """Ollama 서버 연결 확인"""
    try:
        response = requests.get(f"{OLLAMA_URL}/api/tags", timeout=5)
        return response.status_code == 200
    except:
        return False


def stream_response(prompt: str) -> tuple[str, Dict]:
    """스트리밍 방식으로 응답 받기"""
    url = f"{OLLAMA_URL}/api/generate"

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": True
    }

    full_response = ""
    metadata = {}

    try:
        response = requests.post(url, json=payload, stream=True, timeout=120)

        if response.status_code == 200:
            for line in response.iter_lines():
                if line:
                    chunk = json.loads(line)
                    if 'response' in chunk:
                        text = chunk['response']
                        full_response += text
                        yield text

                    if chunk.get('done', False):
                        metadata = {
                            'eval_count': chunk.get('eval_count'),
                            'total_duration': chunk.get('total_duration'),
                        }
                        break
        else:
            yield f"[red]Error: {response.status_code}[/red]"

    except Exception as e:
        yield f"[red]Exception: {str(e)}[/red]"

    return full_response, metadata


def display_welcome():
    """환영 메시지"""
    welcome_text = """
# 🤖 LLM Chat Interface

**Ollama** 기반 대화형 인터페이스입니다.

### 명령어
- `/help` - 도움말 표시
- `/history` - 대화 기록 보기
- `/clear` - 화면 지우기
- `/stats` - 세션 통계
- `/quit` 또는 `/exit` - 종료

질문을 입력하세요!
"""
    console.print(Panel(Markdown(welcome_text), border_style="blue", title="Welcome"))


def display_thinking():
    """생각 중 표시"""
    return Spinner("dots", text="[yellow]생각하는 중...[/yellow]", style="yellow")


def display_user_message(message: str):
    """사용자 메시지 표시"""
    panel = Panel(
        message,
        title="[cyan]👤 You[/cyan]",
        border_style="cyan",
        box=box.ROUNDED,
        padding=(1, 2)
    )
    console.print(panel)


def display_assistant_message(message: str):
    """어시스턴트 메시지 표시 (마크다운 렌더링)"""
    # 메시지가 코드를 포함할 수 있으므로 마크다운으로 렌더링
    panel = Panel(
        Markdown(message),
        title="[green]🤖 Assistant[/green]",
        border_style="green",
        box=box.ROUNDED,
        padding=(1, 2)
    )
    console.print(panel)


def display_streaming_message(prompt: str):
    """스트리밍 메시지 표시"""
    full_text = ""

    with Live(
        Panel(
            display_thinking(),
            title="[green]🤖 Assistant[/green]",
            border_style="green",
            box=box.ROUNDED
        ),
        refresh_per_second=10,
        console=console
    ) as live:

        for chunk in stream_response(prompt):
            if isinstance(chunk, str) and not chunk.startswith("[red]"):
                full_text += chunk
                # 실시간으로 텍스트 업데이트
                live.update(
                    Panel(
                        full_text,
                        title="[green]🤖 Assistant[/green]",
                        border_style="green",
                        box=box.ROUNDED,
                        padding=(1, 2)
                    )
                )
            else:
                # 에러 메시지
                live.update(
                    Panel(
                        chunk,
                        title="[red]❌ Error[/red]",
                        border_style="red",
                        box=box.ROUNDED
                    )
                )
                return None

    return full_text


def handle_command(command: str, session: ChatSession) -> bool:
    """명령어 처리 (True: 계속, False: 종료)"""
    command = command.lower().strip()

    if command in ["/quit", "/exit", "/q"]:
        console.print("\n[yellow]👋 세션을 종료합니다.[/yellow]\n")
        return False

    elif command == "/help":
        display_welcome()

    elif command == "/history":
        console.print(Panel(
            session.get_history_text(),
            title="📜 대화 기록 (최근 5개)",
            border_style="blue"
        ))

    elif command == "/clear":
        console.clear()
        display_welcome()

    elif command == "/stats":
        console.print(Panel(
            session.get_stats(),
            title="📊 세션 통계",
            border_style="magenta"
        ))

    else:
        console.print(f"[red]알 수 없는 명령어: {command}[/red]")
        console.print("[dim]도움말: /help[/dim]")

    return True


def main():
    """메인 함수"""
    console.clear()

    # 연결 확인
    with console.status("[yellow]Ollama 서버 연결 확인 중...[/yellow]"):
        if not check_ollama_connection():
            console.print(Panel(
                "[red]❌ Ollama 서버에 연결할 수 없습니다.[/red]\n\n"
                "다음 명령어로 서버를 시작하세요:\n"
                "[cyan]docker-compose up -d[/cyan]",
                title="Connection Error",
                border_style="red"
            ))
            return

    console.print("[green]✓[/green] Ollama 서버 연결됨\n")

    # 환영 메시지
    display_welcome()

    # 세션 시작
    session = ChatSession()

    try:
        while True:
            # 사용자 입력
            console.print()  # 빈 줄
            user_input = Prompt.ask(
                "[bold cyan]You[/bold cyan]",
                default=""
            ).strip()

            if not user_input:
                continue

            # 명령어 처리
            if user_input.startswith("/"):
                if not handle_command(user_input, session):
                    break
                continue

            # 사용자 메시지 표시
            display_user_message(user_input)
            session.add_message("user", user_input)

            # AI 응답 (스트리밍)
            console.print()  # 빈 줄
            start_time = time.time()
            response = display_streaming_message(user_input)
            elapsed = time.time() - start_time

            if response:
                session.add_message("assistant", response)

                # 성능 메트릭 표시
                console.print(f"\n[dim]⏱️  {elapsed:.2f}초[/dim]")

    except KeyboardInterrupt:
        console.print("\n\n[yellow]👋 Ctrl+C로 종료합니다.[/yellow]\n")
    except Exception as e:
        console.print(f"\n[red]오류 발생: {str(e)}[/red]\n")


if __name__ == "__main__":
    main()
