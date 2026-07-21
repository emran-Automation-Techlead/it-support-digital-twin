import re

SUPERVISOR_DEBATE_TRIGGERS = {
    "impossible_timeline": {
        "detect": r"(?i)(30 minutes|1 hour|immediately|right now|urgent deadline)",
        "response_template": "I understand the urgency. Here's what's realistic: [realistic timeline]. Here's how I can bridge the gap: [workaround]."
    },
    "repeated_issue": {
        "detect": r"(?i)(third|second|again|still|not fixed|keeps happening)",
        "response_template": "Third time is unacceptable. Let me find out why we missed this before. [Root cause diagnosis]."
    },
    "security_concern": {
        "detect": r"(?i)(bypass|skip|workaround the security|disable verification)",
        "response_template": "I can't do that for security reasons. Here's why: [explanation]. Here's the secure alternative: [solution]."
    },
    "system_blame": {
        "detect": r"(?i)(system is broken|system sucks|your system|IT department is useless)",
        "response_template": "I hear the frustration. Let me diagnose if this is a system issue or configuration issue. [Diagnostic questions]."
    }
}


def detect_trigger(text: str) -> str | None:
    for trigger in SUPERVISOR_DEBATE_TRIGGERS.values():
        if re.search(trigger["detect"], text):
            return trigger["response_template"]
    return None
