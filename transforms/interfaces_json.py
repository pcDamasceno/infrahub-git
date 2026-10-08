from typing import Any

from infrahub_sdk.transforms import InfrahubTransform

from ..lib.naming import interface_label


class InterfacesJson(InfrahubTransform):
    query = "device_config"

    async def transform(self, data: dict) -> Any:
        device = data["NetworkDevice"]["edges"][0]["node"]
        name = device["name"]["value"]
        return {
            "device": name,
            "interfaces": [
                interface_label(name, edge["node"]["name"]["value"]) for edge in device["interfaces"]["edges"]
            ],
        }
