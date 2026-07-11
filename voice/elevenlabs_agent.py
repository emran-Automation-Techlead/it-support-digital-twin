import os
import webbrowser
from pathlib import Path

from dotenv import load_dotenv

import ui

load_dotenv()

API_KEY = os.getenv("ELEVENLABS_API_KEY")
AGENT_ID = os.getenv("ELEVENLABS_AGENT_ID")

WIDGET_TEMPLATE = Path(__file__).parent / "widget.html"
WIDGET_RENDERED = Path(__file__).parent / "widget_rendered.html"
PLACEHOLDER = "YOUR_AGENT_ID"


def credentials_missing() -> bool:
    # The web widget only needs the agent ID - the API key is optional
    # and unused in this mode.
    return not AGENT_ID


def start_voice_session():
    if credentials_missing():
        ui.print_warning("⚠️  Missing credentials. Copy .env.example to .env and add your keys.")
        return

    template = WIDGET_TEMPLATE.read_text(encoding="utf-8")
    rendered = template.replace(PLACEHOLDER, AGENT_ID)
    WIDGET_RENDERED.write_text(rendered, encoding="utf-8")

    webbrowser.open(WIDGET_RENDERED.resolve().as_uri())
    ui.print_success("Alex is ready in your browser. Speak after the greeting.")


if __name__ == "__main__":
    start_voice_session()
