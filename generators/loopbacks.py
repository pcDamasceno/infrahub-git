from infrahub_sdk.generator import InfrahubGenerator

from lib.naming import loopback_name


class Loopbacks(InfrahubGenerator):
    async def generate(self, data: dict) -> None:
        device = data["NetworkDevice"]["edges"][0]["node"]
        interface = await self.client.create(
            kind="NetworkInterface",
            data={"name": loopback_name(0), "description": "Router ID", "device": device["id"]},
        )
        await interface.save(allow_upsert=True)
