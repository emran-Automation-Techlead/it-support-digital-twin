import os

from dotenv import load_dotenv

import ui
from voice.audio_utils import describe_audio_devices, has_input_device, has_output_device

load_dotenv()

API_KEY = os.getenv("ELEVENLABS_API_KEY")
AGENT_ID = os.getenv("ELEVENLABS_AGENT_ID")


def credentials_missing() -> bool:
    return not API_KEY or not AGENT_ID


def start_voice_session():
    if credentials_missing():
        ui.print_warning("⚠️  Missing credentials. Copy .env.example to .env and add your keys.")
        return

    from elevenlabs.client import ElevenLabs
    from elevenlabs.conversational_ai.conversation import Conversation
    from elevenlabs.conversational_ai.default_audio_interface import DefaultAudioInterface

    if not has_input_device() or not has_output_device():
        ui.print_error("No microphone/speaker detected on this system. Voice mode requires audio hardware.")
        return

    ui.print_info(f"Audio devices: {describe_audio_devices()}")
    ui.print_info("Connecting to ElevenLabs Conversational AI (Alex)...")

    client = ElevenLabs(api_key=API_KEY)

    conversation = Conversation(
        client,
        AGENT_ID,
        requires_auth=True,
        audio_interface=DefaultAudioInterface(),
        callback_agent_response=lambda text: ui.print_success(f"Alex: {text}"),
        callback_user_transcript=lambda text: ui.print_info(f"You: {text}"),
        callback_end_session=lambda: ui.print_warning("Voice session ended."),
    )

    try:
        conversation.start_session()
        ui.print_success("Voice session started. Speak naturally. Press Ctrl+C to end.")
        conversation.wait_for_session_end()
    except KeyboardInterrupt:
        ui.print_info("Ending voice session...")
        conversation.end_session()
    except Exception as e:
        ui.print_error(f"Voice session failed: {e}")


if __name__ == "__main__":
    start_voice_session()
