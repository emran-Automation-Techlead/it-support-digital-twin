import sounddevice as sd


def has_input_device() -> bool:
    try:
        devices = sd.query_devices()
    except Exception:
        return False
    return any(d.get("max_input_channels", 0) > 0 for d in devices)


def has_output_device() -> bool:
    try:
        devices = sd.query_devices()
    except Exception:
        return False
    return any(d.get("max_output_channels", 0) > 0 for d in devices)


def describe_audio_devices() -> str:
    try:
        default_in, default_out = sd.default.device
        devices = sd.query_devices()
        in_name = devices[default_in]["name"] if default_in is not None and default_in >= 0 else "none"
        out_name = devices[default_out]["name"] if default_out is not None and default_out >= 0 else "none"
        return f"input='{in_name}', output='{out_name}'"
    except Exception as e:
        return f"unavailable ({e})"
