from infrahub_sdk.node import InfrahubNode


def device_names(devices: list[InfrahubNode]) -> list[str]:
    return sorted(device.name.value for device in devices)
