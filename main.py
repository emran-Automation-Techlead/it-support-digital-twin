from agent import Agent
import ui
from voice.elevenlabs_agent import credentials_missing, start_voice_session

EXIT_WORDS = {"exit", "quit", "bye", "q"}

BANNER = """╔══════════════════════════════════╗
║   IT Support Digital Twin        ║
║   Powered by ElevenLabs          ║
╚══════════════════════════════════╝"""


def print_banner():
    ui.console.print(BANNER, style="bold cyan")
    ui.console.print()
    ui.console.print("[1] Text Mode")
    ui.console.print("[2] Voice Mode (Imran - ElevenLabs)")
    ui.console.print()


def select_mode() -> str:
    while True:
        choice = ui.prompt("Select mode [1/2]: ").strip()
        if choice in ("1", "2"):
            return choice
        ui.print_warning("Please enter 1 or 2.")


def run_text_mode():
    ui.print_info(
        "Type your IT issue in plain English (e.g. 'check my vpn', 'reset my "
        "password', 'my computer is slow'). Type 'exit' to quit.\n"
    )

    agent = Agent()

    while True:
        try:
            text = ui.prompt("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            ui.print_info("\nGoodbye.")
            break

        if not text:
            continue

        if text.lower() in EXIT_WORDS:
            ui.print_success("Goodbye.")
            break

        try:
            agent.handle(text)
        except Exception as e:
            ui.print_error(f"Something went wrong handling that request: {e}")

        ui.console.print()


def run_voice_mode():
    if credentials_missing():
        ui.print_warning("⚠️  Missing credentials. Copy .env.example to .env and add your keys.")
        return
    start_voice_session()


def main():
    print_banner()
    choice = select_mode()

    if choice == "2":
        run_voice_mode()
    else:
        run_text_mode()


if __name__ == "__main__":
    main()
