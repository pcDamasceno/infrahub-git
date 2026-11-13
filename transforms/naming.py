def loopback_name(index: int) -> str:
    return f"Loopback{index}"


def interface_label(device: str, interface: str) -> str:
    return f"{device}:{interface}"
