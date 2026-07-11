from agent import Agent
import ui

EXIT_WORDS = {"exit", "quit", "bye", "q"}


def main():
    ui.print_header()
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


if __name__ == "__main__":
    main()
